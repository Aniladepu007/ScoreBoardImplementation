module cla(input [15:0]a, input [15:0]b,output [16:0]out);

//reg [16:0]out;
//integer i;

wire [1:0]w[0:16], L1[0:15], L2[0:15], L3[0:15], L4[0:15];
//final carry values
wire L5[15:0];

genvar q;
generate    for(q=0; q<=15; q=q+1) begin
                  current_status s(.a(a[q]),.b(b[q]),.t(w[q+1]));
            end
endgenerate

assign w[0] = 0;

generate    for(q=0;q<=14;q=q+1) begin
                  look_ahead l(.s(w[15-q]),.f(w[14-q]),.o(L1[q]));
            end
endgenerate

assign L1[15] = w[0];

generate    for(q=0;q<=13;q=q+1) begin
                  look_ahead l(.s(L1[q]),.f(L1[q+2]),.o(L2[q]));
            end
endgenerate

assign L2[14] = L1[14];
assign L2[15] = L1[15];

generate    for(q=0;q<=11;q=q+1) begin
                  look_ahead l(.s(L2[q]),.f(L2[q+4]),.o(L3[q]));
            end
endgenerate

assign {L3[12], L3[13], L3[14], L3[15]} = {L2[12], L2[13], L2[14], L2[15]};

generate    for(q=0;q<=7;q=q+1) begin
                  look_ahead l(.s(L3[q]),.f(L3[q+8]),.o(L4[q]));
            end
endgenerate

generate    for(q=8;q<=15;q=q+1) begin
                  assign L4[q] = L3[q];
            end
endgenerate

generate    for(q=0;q<=15;q=q+1) begin
                  assign L5[q] = a[q] ^ b[q] ^ L4[15-q][0];
            end
endgenerate

generate
      for(q=0; q<=15; q=q+1) begin
            assign out[q] = L5[q];
      end
      assign out[16] = w[16];
endgenerate

//always @(*) begin
      //out[16] = (a[15]==1) ? (b != 16'b0 ? 1 : 0) : 0;
//end

endmodule

module current_status(input a,input b,output [1:0]t);
      assign {t[0],t[1]} = {a || b , a && b};
endmodule

module look_ahead(input [1:0]s, input [1:0]f,output [1:0]o);
wire [1:0]o;
      assign o[1] = (s[1] & s[0] & !f[1]) | (s[0] & f[1] & f[0]);
      assign o[0] = (s[1] & s[0] & !f[1] & !f[0]) | (f[0] & s[0]);
endmodule
