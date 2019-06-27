module cla(input [15:0]a, input [15:0]b,output [16:0]out);

reg [16:0]out;
integer c1[15:0],c[16:0];
integer i,temp,j;

//0=k
//1=g
//2=p

always @(a )
begin
   for(i=0; i<=15; i=i+1) begin
     temp = a[i] ^ b[i];
      if( temp == 1 ) begin
            c1[i] = 2;
      end
      else begin
            c1[i] = a[i];
      end
   end
end


always@( a ) begin
      for(i=0;i<=15;i=i+1)
            c[i] = c1[15-i];
c[16]=0;
end

always @(a )
begin
for(j=0; j<=4; j=j+1) begin
      for(i=1; i<=16; i=i+1) begin
            if(i+2**j <= 16) begin
                  if( c[i]==2 ) begin
                        c[i] = c[i+2**j];
                  end
                  else
                        c[i] = c[i];
            end
      end
end
end


always @(a )  begin
for(i=0; i<16; i=i+1) begin
      c[16-i] = a[i] ^ b[i] ^ c[16-i];
end
end

always @(a or b)
begin
for(i=0; i<=16; i=i+1) begin
      out[i] = c[16-i];
end
end

endmodule
