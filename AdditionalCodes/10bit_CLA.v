module cla( input [9:0]a, input [9:0]b, output [10:0]out );
      reg [10:0] out;
      integer i;
      wire [1:0]w[0:10], L1[0:9], L2[0:9], L3[0:9], L4[0:9];
      //final carry values
      wire L5[9:0];
      genvar q;

      generate    for( q=0; q<=9; q=q+1 ) begin
                        current_status s(.a(a[q]),.b(b[q]),.t(w[q+1]));
                  end
      endgenerate
      assign w[0] = 0;

      generate    for(q=0;q<=8;q=q+1) begin
                        look_ahead l(.s(w[9-q]),.f(w[8-q]),.o(L1[q]));
                  end
      endgenerate
      assign L1[9] = w[0];

      generate    for(q=0;q<=7;q=q+1) begin
                        look_ahead l( .s(L1[q]),.f(L1[q+2]),.o(L2[q]) );
                  end
      endgenerate
      assign {L2[8],L2[9]} = {L1[8],L1[9]};

      generate    for(q=0;q<=5;q=q+1) begin
                        look_ahead l(.s(L2[q]),.f(L2[q+4]),.o(L3[q]));
                  end
      endgenerate
      assign {L3[6], L3[7], L3[8], L3[9]} = {L2[6], L2[7], L2[8], L2[9]};

      generate    for(q=0;q<=1;q=q+1) begin
                        look_ahead l(.s(L3[q]),.f(L3[q+8]),.o(L4[q]));
                  end
      endgenerate
      generate    for( q=2;q<=9;q=q+1 ) begin
                        assign L4[q] = L3[q];
                  end
      endgenerate
      generate    for(q=0;q<=9;q=q+1) begin
                        assign L5[q] = a[q] ^ b[q] ^ L4[9-q][0];
                  end
      endgenerate
      always @(*) begin
            for(i=0; i<=9; i=i+1) begin
                  out[i] = L5[i];
            end
            out[10] = w[10];
      end
endmodule

module current_status(input a,input b,output [1:0]t);
      assign {t[0],t[1]} = {a || b , a && b};
endmodule

module look_ahead(input [1:0]s, input [1:0]f,output [1:0]o);
      assign {o[0], o[1]} = {((s[1] & s[0] & !f[1] & !f[0]) | (f[0] & s[0])) , ((s[1] & s[0] & !f[1]) | (s[0] & f[1] & f[0]))};
endmodule
