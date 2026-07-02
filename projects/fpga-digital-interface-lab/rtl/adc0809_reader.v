`timescale 1ns / 1ps

module adc0809_reader #(
    parameter integer SETUP_CYCLES = 4
) (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       start,
    input  wire       eoc,
    input  wire [7:0] adc_data,
    output reg        ale,
    output reg        start_conv,
    output reg        oe,
    output reg        busy,
    output reg        done,
    output reg  [7:0] sample
);
    localparam [2:0] S_IDLE      = 3'd0;
    localparam [2:0] S_LATCH     = 3'd1;
    localparam [2:0] S_START     = 3'd2;
    localparam [2:0] S_WAIT_LOW  = 3'd3;
    localparam [2:0] S_WAIT_HIGH = 3'd4;
    localparam [2:0] S_READ      = 3'd5;

    reg [2:0] state;
    reg [7:0] setup_count;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state      <= S_IDLE;
            setup_count <= 8'd0;
            ale        <= 1'b0;
            start_conv <= 1'b0;
            oe         <= 1'b0;
            busy       <= 1'b0;
            done       <= 1'b0;
            sample     <= 8'd0;
        end else begin
            ale        <= 1'b0;
            start_conv <= 1'b0;
            oe         <= 1'b0;
            done       <= 1'b0;

            case (state)
                S_IDLE: begin
                    busy <= 1'b0;
                    if (start) begin
                        busy        <= 1'b1;
                        ale         <= 1'b1;
                        setup_count <= 8'd0;
                        state       <= S_LATCH;
                    end
                end
                S_LATCH: begin
                    ale <= 1'b1;
                    if (setup_count == SETUP_CYCLES - 1) begin
                        setup_count <= 8'd0;
                        state       <= S_START;
                    end else begin
                        setup_count <= setup_count + 1'b1;
                    end
                end
                S_START: begin
                    start_conv <= 1'b1;
                    state      <= S_WAIT_LOW;
                end
                S_WAIT_LOW: begin
                    if (!eoc) begin
                        state <= S_WAIT_HIGH;
                    end
                end
                S_WAIT_HIGH: begin
                    if (eoc) begin
                        state <= S_READ;
                    end
                end
                S_READ: begin
                    oe     <= 1'b1;
                    sample <= adc_data;
                    done   <= 1'b1;
                    busy   <= 1'b0;
                    state  <= S_IDLE;
                end
                default: state <= S_IDLE;
            endcase
        end
    end
endmodule
