module left_shift_tb();

reg [10:0]a;
reg [3:0]s;
wire [10:0]out;

left_shifter_11bit obj(.in(a), .size(s), .out(out));

initial begin
      a = 5;
      s = 4;
end

initial begin
      $dumpfile("ls.vcd");
      $dumpvars(0,left_shift_tb);
      $monitor("%d, %d",a, out);
end


endmodule
