clc
clear
close all

rcos = [6, 3, -4, -10, -8, 2, 16, 23, 13, -13, -40, -47, -15, 57, 149, 226, 255, 226, 149, 57, -15, -47, -40, -13, 13, 23, 16, 2, -8, -10, -4, 3, 6];

file = fopen('output_2022-07-06_15-12-18.log', 'r');
data = fscanf(file, '%s');
fclose(file);

data = reshape(data, 4, length(data)/4)';
i_data = data(1:2:end, :);
q_data = data(2:2:end, :);

i_dec = hex2signed(i_data);
q_dec = hex2signed(q_data);

i_samples = upfirdn(i_dec(2:end), rcos, 1, 4) / sum(rcos.^2);
q_samples = upfirdn(q_dec(2:end), rcos, 1, 4) / sum(rcos.^2);
i_samples = i_samples(10:end-4);
q_samples = q_samples(10:end-4);

subplot(1,3,1)
plot(i_dec)
hold on
plot(q_dec)

subplot(1,3,2)
plot(i_samples)
hold on
plot(q_samples)

legend('I', 'Q')

subplot(1,3,3)
scatter(i_samples, q_samples, 'x')

function reversed_bin = reverse_bin(bin_str)
  
  for i = 1:length(bin_str)
    
    if bin_str(i) == '1'
      reversed_bin(i) = '0';
    elseif bin_str(i) == '0'
      reversed_bin(i) = '1';
    else
      error('String is not binary!')
    end
    
  end
  
end

function signed_dec = bin2signed(bin_str)
 
  if bin_str(1) == '1'
    
    reversed_bin_str = reverse_bin(bin_str);
    signed_dec = -(bin2dec(reversed_bin_str) + 1);
    
  else
    
    signed_dec = bin2dec(bin_str);
    
  end
  
end

function signed_dec = hex2signed(hex_str)
  signed_dec = zeros(height(hex_str), 1);
  for i = 1:height(hex_str)
    bin_str = dec2bin(hex2dec(hex_str(i, :)), 16);
    signed_dec(i) = bin2signed(bin_str);
  end
end
