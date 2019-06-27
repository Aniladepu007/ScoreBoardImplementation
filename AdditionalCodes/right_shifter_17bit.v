module right_shifter_17bit(input [16:0]in, input [4:0]size, output [16:0]out);
reg [16:0]out;
integer i;
always @ (in) begin
      for(i=size; i<=16; i=i+1)
            out[i-size] = in[i];
      for(i=17-size; i<=16; i=i+1)
            out[i] = 1'b0;
end
endmodule
