module right_shifter_11bit(input [10:0]in, input [3:0]size, output [10:0]out);
reg [10:0]out;
integer i;
always @ (in) begin
      for(i=size; i<=10; i=i+1)
            out[i-size] = in[i];
      for(i=11-size; i<=10; i=i+1)
            out[i] = 1'b0;
end
endmodule
