`timescale 1ns / 1ps

module edge_detector (
    input  wire clk,
    input  wire rst_n,
    input  wire signal_in,
    output wire rising_edge,
    output wire falling_edge
);
    reg signal_d;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            signal_d <= 1'b0;
        end else begin
            signal_d <= signal_in;
        end
    end

    assign rising_edge  =  signal_in & ~signal_d;
    assign falling_edge = ~signal_in &  signal_d;
endmodule
