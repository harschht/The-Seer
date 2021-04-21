
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% The Straw Hats: The Seer - EE493 Senior Design                     %%%%
%% JTC Path Loss with Added Noise Simulation                          %%%%
%% 3 Antenna Array, Power Only - Simulated Data for Neural Network    %%%%
%% Author: Victor Madrid & Tate Harsch-Hudspeth                       %%%%
%% Last Edit Made: 04/14/2021                                         %%%%
%% University: Sonoma State University                                %%%% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Define Variables:
f = 750*10^6; % In Hz
% htx = 50 - Model is based on transmitter (Tx) height htx in meters
% hrx = 1.5 - Model is based on receiver (Rx) height hrx in meters
ptx = 44; % Tx output power in dBm, equals 25W.
v = 1; % Variance (noise)
lambda = (3* 10^8) / f; % Wavelength in meters

% Random Distance Generator:
% Below are the possible distances that our Tx could be from the Rx, in cm.
x = randperm(800,100); % n random #s that do not repeat between 1-800 
% Exlude numbers under 125 cm (too close to base station)
for i=(1:length(x))
    if x(i)<=125
        x(i) = x(i)+125;
    end
    % Now lets make x randomly negative:
    xrandnum = randperm(2,1);
    if xrandnum==2
        x(i) = x(i)*-1;
    end
end
y = randperm(800,100); % n random #s that do not repeat between 1-800
% Exlude numbers under 125 cm (too close to base station)
for i=(1:length(y))
    if y(i)<=125
        y(i) = y(i)+125;
    end
end

% Due to the linear nature of the array, only posative y values are
% considered. The linear array ensures no shadowing will occurr between the
% antennas aside from the extremes at y = 0. These extremes will not be
% considered (no cell phone would be so close to the base station). 5G base
% stations have these arrays facing each quadrant to allow full coverage.

% Cycle through coordinate pairs and determine the linear distance between
% the Tx and the various antennas of the Rx:
d = [];
x_answer = [];
y_answer = [];
r = [];
theta = [];
reldist = [];
lf = []; % Floor and wall penetration loss coeff (residential)
for i=(1:length(x))
    centerx = x(i);
    centery = y(i);
    rgg = sqrt((centerx)^2 + (centery)^2);
    thetagg = atan2(centery,centerx); 
    thetagg = thetagg * (180/pi);
    if thetagg < 0 
        thetagg = thetagg + 360;
    end
    r = [r,rgg];
    theta = [theta,thetagg];
    x_answer = [x_answer,centerx];
    y_answer = [y_answer,centery];
    
    % Define the distances between the simulated Tx and the different
    % antennas:
    if centerx > 0
        rightright = centerx - (lambda / 2);
        dist = sqrt(rightright^2 + centery^2);
        d = [d,dist];
        dist = rgg;
        d = [d,dist];
        leftleft = centerx + (lambda / 2);
        dist = sqrt(leftleft^2 + centery^2);
        d = [d,dist];
    elseif centerx < 0
        rightright = (-1*centerx) + (lambda / 2);
        dist = sqrt(rightright^2 + centery^2);
        d = [d,dist];
        dist = rgg;
        d = [d,dist];
        leftleft = (-1*centerx) - (lambda / 2);
        dist = sqrt(leftleft^2 + centery^2);
        d = [d,dist];
    end
    
    % n = Number of walls between the Tx and Rx
    if (centerx > 550) && (centery > 550)
        n = 2;
        lf_o = 4 * n;
        lf = [lf,lf_o,lf_o,lf_o];
    elseif (centerx < -550) && (centery > 550)
        n = 3;
        lf_o = 4 * n;
        lf = [lf,lf_o,lf_o,lf_o];
    elseif (centerx > 600) && (centery < 600)
        n = 1;
        lf_o = 4 * n;
        lf = [lf,lf_o,lf_o,lf_o];
    else
        n = 0;
        lf_o = 4 * n;
        lf = [lf,lf_o,lf_o,lf_o];
    end
end
% Scaling from cm to meters
d = d / 100;
r = r / 100;
x_answer = x_answer / 100;
y_answer = y_answer / 100;

%Defining the Channel: JTC Indoor Propagation Model w/ added noise
a = 38; % Fixed enviromental dependent loss factor (38 for residential)
b = 28; % Distance dependent loss factor (28 for residential)
% lf = Floor and wall penetration loss coeff (residential)
sigma = 8; % lognormal shadowing (residential)
total_loss = [];
for u=(1:length(d))
    dist = d(u);
    ploss = a + (b * (log(dist))) + lf(u) + sigma;
    total_loss = [total_loss,ploss];
end

prx = ptx - total_loss; % Tx power - loss = Rx power
prx = 1000 * (10.^(prx./10)); % Convert from dBm to Watts
%pre_noise_prx = prx;

% Adding Noise:
% Below we add a realistic amount of white gaussian noise
nfl = .00001; % Noise floor low power in Watts ~ -50 dB
nfh = .0001; % Noise floor high power in Watts ~ -40 dB
noise_len = length(d);
noise = sqrt(v) * ((nfh-nfl).*rand(1,noise_len) + nfl);
prx = prx + noise;

pre_prx = ones(length(r),3);
for i=(1:length(r))
    c1 = 3*i-2;
    c2 = 3*i-1;
    c3 = 3*i;
    if c1 > length(prx)
        break;
    end
    pre_prx(i,1) = prx(c1);
    pre_prx(i,2) = prx(c2);
    pre_prx(i,3) = prx(c3);
end

% Shaping the array in preperation for the Neural Network:
% We want a 5 column tensor with the first 3 consisting of inputs and the
% last two consisitng of (x,y) or (r,theta). Although uncecessary in this
% simulation, we leave the structure in case one would need to reintroduce
% the relative phase difference.
prx_len = length(pre_prx);
power_nophase = ones(prx_len,3);
for i=(1:prx_len)
        power_nophase(i,1) = pre_prx(i,1);
        power_nophase(i,2) = pre_prx(i,2);
        power_nophase(i,3) = pre_prx(i,3);
end
new_power = ones(prx_len,5);
for z=(1:prx_len)
    for p=(1:3)
        new_power(z,p) = power_nophase(z,p) .* new_power(z,p);
    end
    new_power(z,4) = r(z);
    new_power(z,5) = theta(z);
    %new_power(z,4) = x_answer(z);
    %new_power(z,5) = y_answer(z);
end

% Lets write the new array of tensors to a CSV file:
csvwrite('JTC_w_added_noise_3P.csv',new_power)

%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
