//has rounding modes involved too(approximations)!
`include "new_wtm.v"
module fpm(input [15:0]a, input [15:0]b, output[15:0]out);
wire [10:0]var1,var2;
wire shift;
wire isSignEqual;

//for wtm
wire [15:0] var3, var4;
wire [32:0] wtm_out;
assign isSignEqual = a[15]==b[15] ? 1 : 0;

assign out[15] = !isSignEqual ? 1 : a[15];

assign {var1[9:0], var2[9:0]} = {a[9:0], b[9:0]};
assign var1[10] = 1;
assign var2[10] = 1;
assign var3 = var1;
assign var4 = var2;

wallace_mul obj(var3, var4, wtm_out);
//assign shift = $clog2(wtm_out)-21;
//assign out[14:10] = a[14:10] + b[14:10] - 15 + shift;
assign out[14:10] = wtm_out[21]==1 ? (a[14:10] + b[14:10] - 15 +1) : (a[14:10] + b[14:10] - 15);

assign out[9:0] = wtm_out[21]==1 ? wtm_out[20:11] : wtm_out[19:10];
//assign out[9:0] = wtm_out[21]==1 ? ( wtm_out[10]==1 ? wtm_out[20:11]+2'b10 : wtm_out[20:11] ) : ( wtm_out[10]==1 ? wtm_out[19:10]+2'b10 : wtm_out[19:10] );

endmodule
