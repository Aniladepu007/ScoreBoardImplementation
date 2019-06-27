module cla_tb();
reg [15:0] avector;
reg [15:0] bvector;
wire [16:0] c;

cla obj(
.a(avector),
.b(bvector),
.out(c)
);

initial begin
      avector = 130;
      bvector = 8;
end

initial

begin
$dumpfile("CLA_prefix.vcd");
$dumpvars(0,cla_tb);
$monitor("%d   %d   %d",avector,bvector,c);

//while(!obj.flag);
//$monitor("%d   %d   %d",avector,bvector,obj.c);
end

endmodule
