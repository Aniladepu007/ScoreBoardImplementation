import os
import re

def fpm(a, b):
    if a >= 0:
        s1 = 0
    else:
        s1 = 1
        a = abs(b)
    if b >= 0:
        s2 = 0
    else:
        s2 = 1
        b = abs(b)
    file1 = open("fpm_tb.v", "w")  # creating the tb file
    file1.write('''
module fpm_tb();

reg temp,s1,s2;
reg [15:0] a1,a2;
reg[31:0] b1, b2;
real int1,f1,int2,f2;
integer i,index1=-1,index2=-1,neg_index1,neg_index2;

real f;
integer in,count=9,pos = 31,ind1,ind2,flag=1;


// ieee format
reg [15:0] final1,final2;
wire [15:0] out_put;

fpm obj(.a(final1),.b(final2),.out(out_put));

initial begin
      //inputs here
          //inputs here
          s1 = '''+str(s1)+''';   int1 = '''+str(int(a))+''';     f1 = '''+str(round((a-int(a)), 5))+''';  //a = int1+f1
          s2 = '''+str(s2)+''';   int2 = '''+str(int(b))+''';     f2 = '''+str(round((b-int(b)), 5))+''';  //b = int2+f2
end

initial begin
      if((int1==0 && f1==0) || (int2==0 && f2==0)) begin
            $display("%b",16'b0);
            $finish;
      end

      if((int1 + f1)*(int2 + f2) >=65536) begin
            $display("%f...Inf",(int1 + f1)*(int2 + f2));
            $finish;
      end
end

initial begin
      in = int1;
      for(i=0;i<=15;i=i+1)    begin
            temp = in % 2;
            if(temp)
                  index1 = i;
            a1[i] = temp;
            in = in/2;
      end
      f = f1;
      for(i=31;i>=0;i=i-1) begin
            f = f * 2;
            if(f >= 1) begin
                  b1[i] = 1;
                  if(flag)
                        neg_index1 = i-32;
                  f = f - 1;
                  flag = 0;
            end
            else
                  b1[i] = 0;

      end

//for 2nd float
      in = int2;
      for(i=0;i<=15;i=i+1)    begin
            temp = in % 2;
            if(temp)
                  index2 = i;
            a2[i] = temp;
            in = in/2;
      end
      f = f2; flag = 1;
      for(i=31;i>=0;i=i-1) begin
            f = f * 2;
            if(f >= 1) begin
                  b2[i] = 1;
                  if(flag)
                        neg_index2 = i-32;
                  f = f - 1;
                  flag = 0;
            end
            else
                  b2[i] = 0;
      end

      final1[15] = s1;  final2[15] = s2;
      if(index1 == -1)
            final1[14:10] = 15 + neg_index1;
      else
            final1[14:10] = 15+index1;

      if(index2 == -1)
            final2[14:10] = 15 + neg_index2;
      else
            final2[14:10] = 15+index2;

      ind1 = index1-1;    ind2 = index2-1;

      if(index1 >= 0) begin
      while(count >= 0 && ind1>=0) begin
            final1[count] = a1[ind1];
            ind1 = ind1 - 1;
            count = count - 1;
      end
      end

      if(index1<0)
            pos = 31+neg_index1;

      while(count >= 0) begin
            final1[count] = b1[pos];
            pos = pos - 1;
            count = count - 1;
      end

      //2nd ieee
      count = 9; pos = 31;
      if(index2 >=0) begin
      while(count > 0 && ind2>=0) begin
            final2[count] = a2[ind2];
            ind2 = ind2 - 1;
            count = count - 1;
      end
      end

      if(index2 < 0)
            pos = 31+neg_index2;

      while(count >= 0) begin
            final2[count] = b2[pos];
            pos = pos - 1;
            count = count - 1;
      end
end

integer p;
real sum=0,exp;
reg [63:0] float_out;

    initial begin
          #15;
      exp = out_put[14:10];
      exp = exp-15;
      exp = exp + 1023;
      float_out[62:52] = exp;
      float_out[63] = out_put[15];
      float_out[51:42] = out_put[9:0];
      float_out[41:0] = 42'b0;      
      $display($bitstoreal(float_out));
    end
    endmodule
    ''')
    file1.close()
    os.system(" iverilog fpm.v fpm_tb.v ")
    os.system("vvp a.out>result.txt")

    file = open("result.txt", "r+")
    out = file.read()
    out1 = re.findall(r"[-+]?\d*\.\d+|\d+", out)
    file.truncate(0)
    #os.system("rm result.txt fpm_tb.v")
    file.close()
    return float(out1[0])


def fpa(a, b):
    if a >= 0:
        s1 = 0
    else:
        s1 = 1
        a = abs(b)
    if b >= 0:
        s2 = 0
    else:
        s2 = 1
        b = abs(b)
    file1 = open("fpa_tb.v", "w")  # creating the tb file
    file1.write('''
    module fpa_tb();
    reg temp,s1,s2;
    reg [15:0] a1,a2;
    reg[31:0] b1, b2;
    real int1,f1,int2,f2;
    integer i,index1=-1,index2=-1,neg_index1,neg_index2;
    
    real f;
    integer in,count=9,pos = 31,ind1,ind2,flag=1;
    
    // ieee format
    reg [15:0] final1,final2;
    wire [15:0] out_put;
    
    fpa obj(.a(final1),.b(final2),.out(out_put)
    );
    
    initial begin
          //inputs here
          s1 = '''+str(s1)+''';   int1 = '''+str(int(a))+''';     f1 = '''+str(round((a-int(a)), 5))+''';  //a = int1+f1
          s2 = '''+str(s2)+''';   int2 = '''+str(int(b))+''';     f2 = '''+str(round((b-int(b)), 5))+''';  //b = int2+f2
          if(s1==s2)
                if(int1 + int2 + f1 + f2 >=65536) begin
                      if(!s1)
                            $display("Inf");
                      else
                            $display("-Inf");
                      $finish;
                end
    end
    
    initial begin
    if(int1==0 && f1==0) begin
          if(s2) begin
                $display("-%f",int2+f2);
                $finish;
          end
          else begin
                $display("+%f",int2+f2);
                $finish;
          end
    end
    else if(int2==0 && f2==0) begin
          if(s1) begin
                $display("-%f",int1+f1);
                $finish;
          end
          else begin
                $display("+%f",int1+f1);
                $finish;
          end
    end
    end
    
    initial begin
          in = int1;
          for(i=0;i<=15;i=i+1)    begin
                temp = in % 2;
                if(temp)
                      index1 = i;
                a1[i] = temp;
                in = in/2;
          end
          f = f1;
          for(i=31;i>=0;i=i-1) begin
                f = f * 2;
                if(f >= 1) begin
                      b1[i] = 1;
                      if(flag)
                            neg_index1 = i-32;
                      f = f - 1;
                      flag = 0;
                end
                else
                      b1[i] = 0;
    
          end
    
    //for 2nd float
          in = int2;
          for(i=0;i<=15;i=i+1)    begin
                temp = in % 2;
                if(temp)
                      index2 = i;
                a2[i] = temp;
                in = in/2;
          end
          f = f2; flag = 1;
          for(i=31;i>=0;i=i-1) begin
                f = f * 2;
                if(f >= 1) begin
                      b2[i] = 1;
                      if(flag)
                            neg_index2 = i-32;
                      f = f - 1;
                      flag = 0;
                end
                else
                      b2[i] = 0;
          end
    
          final1[15] = s1;  final2[15] = s2;
          if(index1 == -1)
                final1[14:10] = 15 + neg_index1;
          else
                final1[14:10] = 15+index1;
    
          if(index2 == -1)
                final2[14:10] = 15 + neg_index2;
          else
                final2[14:10] = 15+index2;
    
          ind1 = index1-1;    ind2 = index2-1;
    
          if(index1 >= 0) begin
          while(count >= 0 && ind1>=0) begin
                final1[count] = a1[ind1];
                ind1 = ind1 - 1;
                count = count - 1;
          end
          end
    
          if(index1<0)
                pos = 31+neg_index1;
    
          while(count >= 0) begin
                final1[count] = b1[pos];
                pos = pos - 1;
                count = count - 1;
          end
    
          //2nd ieee
          count = 9; pos = 31;
          if(index2 >=0) begin
          while(count > 0 && ind2>=0) begin
                final2[count] = a2[ind2];
                ind2 = ind2 - 1;
                count = count - 1;
          end
          end
    
          if(index2 < 0)
                pos = 31+neg_index2;
    
          while(count >= 0) begin
                final2[count] = b2[pos];
                pos = pos - 1;
                count = count - 1;
          end
    end
integer p;
real sum=0,exp;
reg [63:0] float_out;
    
    initial begin
          #15;
      exp = out_put[14:10];
      exp = exp-15;
      exp = exp + 1023;
      float_out[62:52] = exp;
      float_out[63] = out_put[15];
      float_out[51:42] = out_put[9:0];
      float_out[41:0] = 42'b0;
//      $display("%b", float_out);
      $display($bitstoreal(float_out));
  //    $display("%b %f %f %f %f %b %b", out_put, int1, int2, f1, f2, s1, s2);   
    //  $display("%b %b",final1, final2);   
       
    end
    endmodule
    ''')
    file1.close()
    os.system(" iverilog fpa.v fpa_tb.v ")
    os.system("vvp a.out>result.txt")

    file = open("result.txt", "r+")
    out = file.read()
    out1 = re.findall(r"[-+]?\d*\.\d+|\d+", out)
    file.truncate(0)
    #os.system("rm result.txt fpa_tb.v")
    file.close()
    return float(out1[0])


def cla(a, b):
    file1 = open("cla_tb.v", "w")  # creating the tb file
    file1.write('''module cla_tb();
    reg [15:0] avector, bvector;
    wire [16:0] c;

    cla obj(.a(avector),.b(bvector),.out(c));

    initial begin
          avector = ''' + str(a) + ''';  bvector = ''' + str(b) + ''';
    end

    initial begin
        $monitor("%d",c);
    end
    endmodule
    ''')
    file1.close()
    os.system(" iverilog cla_16bit_structural.v cla_tb.v ")
    os.system("vvp a.out>result.txt")

    file = open("result.txt", "r+")
    out = file.read()
    out1 = re.findall(r"[-+]?\d*\.\d+|\d+", out)
    file.truncate(0)
    os.system("rm result.txt cla_tb.v")
    file.close()
    return int(out1[0])


def wtm(a, b):
    if a >= 0:
        s1 = 0
    else:
        s1 = 1
        a = abs(a)
    if b >= 0:
        s2 = 0
    else:
        s2 = 1
        b = abs(b)
    file1 = open("wtm_tb.v", "w")
    file1.write('''module wallace_tb();
    reg [15:0] avector,bvector;
    wire [32:0] c;
    wallace_mul obj(.a(avector),.b(bvector),.out(c));
    
    initial begin
          avector = '''+str(a)+''';
          bvector = '''+str(b)+''';
    end
    
    initial begin
        #5;
          $display("%d",c);
    end
    endmodule
    ''')
    file1.close()
    os.system(" iverilog new_wtm.v wtm_tb.v ")
    os.system("vvp a.out>result.txt")
    file = open("result.txt", "r+")
    out = file.read()
    out1 = re.findall(r"[-+]?\d*\.\d+|\d+", out)
    file.truncate(0)
    #os.system("rm result.txt wtm_tb.v")
    file.close()
    new_out = int(out1[0])
    sign = s1 ^ s2
    if sign:
        return -1*new_out
    else:
        return new_out

