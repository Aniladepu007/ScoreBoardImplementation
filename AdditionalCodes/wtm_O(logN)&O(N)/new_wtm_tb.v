module wallace_tb();
reg [15:0] avector;
reg [15:0] bvector;
wire [32:0] c;
integer i;
wallace_mul obj(
.a(avector),
.b(bvector),
.out(c)
);

initial begin
//      avector = 16'b0000000011011011;
//      bvector = 16'b0000000001100110;
      avector = 65535;
      bvector = 65535;
end

initial begin
      $dumpfile("wallace.vcd");
      $dumpvars(0,wallace_tb);
#10;
      $display(" %d   %d   %d",avector,bvector,c);
end
endmodule
