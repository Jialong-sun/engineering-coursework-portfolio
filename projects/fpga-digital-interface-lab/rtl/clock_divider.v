`timescale 1ns / 1ps

module clock_divider #(
    parameter integer DIVIDE = 50_000_000
) (
    input  wire clk,
    input  wire rst_n,
    output reg  tick,
    output reg  clk_out
);
    localparam integer COUNT_WIDTH = $clog2(DIVIDE);
    reg [COUNT_WIDTH-1:0] count;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count   <= {COUNT_WIDTH{1'b0}};
            tick    <= 1'b0;
            clk_out <= 1'b0;
        end else if (count == DIVIDE - 1) begin
            count   <= {COUNT_WIDTH{1'b0}};
            tick    <= 1'b1;
            clk_out <= ~clk_out;
        end else begin
            count <= count + 1'b1;
            tick  <= 1'b0;
        end
    end
endmodule
