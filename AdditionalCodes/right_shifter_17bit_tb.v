module right_shift_17bit_tb();

reg [16:0]a;
reg [4:0]s;
wire [16:0]out;

right_shifter_17bit obj(.in(a), .size(s), .out(out));

initial begin
      a = 121;
      s = 2;
end

initial begin
      $dumpfile("rs.vcd");
      $dumpvars(0,right_shift_17bit_tb);
      $monitor("%b, %b",a, out);
end


endmodule
