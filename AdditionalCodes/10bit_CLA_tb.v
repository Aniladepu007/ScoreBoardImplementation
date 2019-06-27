module cla_tb();
reg [9:0] avector, bvector;
wire [10:0] c;

cla obj(.a(avector), .b(bvector), .out(c));

initial begin
      avector = 1023;  //edge-cases
      bvector = 13;   //edge-cases
end

initial begin
//      $dumpfile("vamsi.vcd");
//      $dumpvars(0,cla_tb);
      $monitor("%d + %d  =  %d",avector,bvector,c);
end
endmodule
