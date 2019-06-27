module cla32(input [31:0]a, input [31:0]b,output [32:0]out);
wire [1:0]w[0:32], L1[0:31], L2[0:31], L3[0:31], L4[0:31],L5[0:31];
//final carry values
wire L6[31:0];

genvar q;
generate    for(q=0; q<=31; q=q+1) begin
                  current_status s(.a(a[q]),.b(b[q]),.t(w[q+1]));
            end
endgenerate

assign w[0] = 0;

generate    for(q=0;q<=30;q=q+1) begin
                  look_ahead l(.s(w[31-q]),.f(w[30-q]),.o(L1[q]));
            end
endgenerate

assign L1[31] = w[0];

generate    for(q=0;q<=29;q=q+1) begin
                  look_ahead l(.s(L1[q]),.f(L1[q+2]),.o(L2[q]));
            end
endgenerate

assign L2[30] = L1[30];
assign L2[31] = L1[31];

generate    for(q=0;q<=27;q=q+1) begin
                  look_ahead l(.s(L2[q]),.f(L2[q+4]),.o(L3[q]));
            end
endgenerate

assign {L3[28], L3[29], L3[30], L3[31]} = {L2[27], L2[28], L2[30], L2[31]};

generate    for(q=0;q<=23;q=q+1) begin
                  look_ahead l(.s(L3[q]),.f(L3[q+8]),.o(L4[q]));
            end
endgenerate

generate    for(q=24;q<=31;q=q+1) begin
                  assign L4[q] = L3[q];
            end
endgenerate

generate    for(q=0;q<=15;q=q+1) begin
                  look_ahead l(.s(L4[q]),.f(L4[q+16]),.o(L5[q]));
            end
endgenerate

generate    for(q=16;q<=31;q=q+1) begin
                  assign L5[q] = L4[q];
            end
endgenerate

generate    for(q=0;q<=31;q=q+1) begin
                  assign L6[q] = a[q] ^ b[q] ^ L5[31-q][0];
            end
endgenerate

generate    for(q=0;q<=31;q=q+1) begin
                  assign out[q] = L6[q];
            end
            assign out[32] = w[0];
endgenerate
endmodule

module current_status(input a,input b,output [1:0]t);
      assign {t[0],t[1]} = {a || b , a && b};
endmodule

module look_ahead(input [1:0]s, input [1:0]f,output [1:0]o);
wire [1:0]o;
      assign o[1] = (s[1] & s[0] & !f[1]) | (s[0] & f[1] & f[0]);
      assign o[0] = (s[1] & s[0] & !f[1] & !f[0]) | (f[0] & s[0]);
endmodule
