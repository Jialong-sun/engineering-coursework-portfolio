`timescale 1ns / 1ps

module seven_segment_scan (
    input  wire       clk,
    input  wire       rst_n,
    input  wire [3:0] digit0,
    input  wire [3:0] digit1,
    input  wire [3:0] digit2,
    input  wire [3:0] digit3,
    output reg  [3:0] an,
    output reg  [6:0] seg
);
    reg [1:0] scan_index;
    reg [3:0] active_digit;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            scan_index <= 2'b00;
        end else begin
            scan_index <= scan_index + 2'b01;
        end
    end

    always @(*) begin
        case (scan_index)
            2'b00: begin an = 4'b1110; active_digit = digit0; end
            2'b01: begin an = 4'b1101; active_digit = digit1; end
            2'b10: begin an = 4'b1011; active_digit = digit2; end
            default: begin an = 4'b0111; active_digit = digit3; end
        endcase
    end

    always @(*) begin
        case (active_digit)
            4'h0: seg = 7'b1000000;
            4'h1: seg = 7'b1111001;
            4'h2: seg = 7'b0100100;
            4'h3: seg = 7'b0110000;
            4'h4: seg = 7'b0011001;
            4'h5: seg = 7'b0010010;
            4'h6: seg = 7'b0000010;
            4'h7: seg = 7'b1111000;
            4'h8: seg = 7'b0000000;
            4'h9: seg = 7'b0010000;
            4'hA: seg = 7'b0001000;
            4'hB: seg = 7'b0000011;
            4'hC: seg = 7'b1000110;
            4'hD: seg = 7'b0100001;
            4'hE: seg = 7'b0000110;
            default: seg = 7'b0001110;
        endcase
    end
endmodule
