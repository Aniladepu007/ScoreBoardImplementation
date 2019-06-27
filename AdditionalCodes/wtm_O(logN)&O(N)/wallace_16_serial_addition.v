`include "32bit_cla.v"

module wallace_mul(input [15:0]a, input [15:0]b, output [32:0]out);

wire [30:0] m[0:15];
wire [30:0] u[14:0];
wire [31:0] v[14:0];
//wire [31:0] temp;

genvar q,k;
assign m[0] = b[0] == 0 ? 31'b0 : {15'b0,a};
assign m[1] = b[1] == 0 ? 31'b0 : {14'b0,a,1'b0};
assign m[2] = b[2] == 0 ? 31'b0 : {13'b0,a,2'b0};
assign m[3] = b[3] == 0 ? 31'b0 : {12'b0,a,3'b0};
assign m[4] = b[4] == 0 ? 31'b0 : {11'b0,a,4'b0};
assign m[5] = b[5] == 0 ? 31'b0 : {10'b0,a,5'b0};
assign m[6] = b[6] == 0 ? 31'b0 : {9'b0,a,6'b0};
assign m[7] = b[7] == 0 ? 31'b0 : {8'b0,a,7'b0};
assign m[8] = b[8] == 0 ? 31'b0 : {7'b0,a,8'b0};
assign m[9] = b[9] == 0 ? 31'b0 : {6'b0,a,9'b0};
assign m[10] = b[10] == 0 ? 31'b0 : {5'b0,a,10'b0};
assign m[11] = b[11] == 0 ? 31'b0 : {4'b0,a,11'b0};
assign m[12] = b[12] == 0 ? 31'b0 : {3'b0,a,12'b0};
assign m[13] = b[13] == 0 ? 31'b0 : {2'b0,a,13'b0};
assign m[14] = b[14] == 0 ? 31'b0 : {1'b0,a,14'b0};
assign m[15] = b[15] == 0 ? 31'b0 : {a,15'b0};

generate    for(q=0; q<=14; q=q+1) begin
                  assign v[q][0] = 0;
            end
endgenerate

generate    for(q=1; q<=31; q=q+1) begin
                  fa f(1'b0,m[0][q-1],m[1][q-1],u[0][q-1],v[0][q]);
            end
endgenerate

generate    for(k=0; k<=13; k=k+1) begin
                  for(q=1; q<=31; q=q+1) begin
                        fa f(u[k][q-1],v[k][q-1],m[k+2][q-1],u[k+1][q-1],v[k+1][q]);
                  end
            end
endgenerate

//assign temp = {1'b0,u[14]};

cla32 object({1'b0,u[14]},v[14],out);
endmodule

module fa(input a,input b, input c, output s,output o);
//wire w1,w2;
      xor(w1,a,b);      xor(w2,c,w1);
assign s = w2;
      and(w3,a,b);      and(w4,b,c);      and(w5,a,c);
      or(w6,w3,w4);     or(w7,w6,w5);
assign o = w7;
endmodule
