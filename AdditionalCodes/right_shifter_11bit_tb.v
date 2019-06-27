module right_shift_tb();

reg [10:0]a;
reg [3:0]s;
wire [10:0]out;

right_shifter_11bit obj(.in(a), .size(s), .out(out));

initial begin
      a = 121;
      s = 4;
end

initial begin
      $dumpfile("rs_11bit.vcd");
      $dumpvars(0,right_shift_tb);
      $monitor("%b, %b",a, out);
end


endmodule
