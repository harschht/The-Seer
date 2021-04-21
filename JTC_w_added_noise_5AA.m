
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% The Straw Hats: The Seer - EE493 Senior Design                     %%%%
%% JTC Path Loss with Added Noise Simulation                          %%%%
%% Linear 5 Antenna Array - Simulated Data for Neural Network         %%%%
%% Author: Victor Madrid & Tate Harsch-Hudspeth                       %%%%
%% Last Edit Made: 03/30/2021                                         %%%%
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
x = randperm(1400,500); % N random #s that do not repeat between 1-1400 
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
y = randperm(1400,500); % N random #s that do not repeat between 1-1400
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
    rgg = rgg / 100; % Scaling from cm to meters
    r = [r,rgg];
    thetagg = atan2(centery,centerx); 
    thetagg = thetagg * (180/pi);
    if thetagg < 0 
        thetagg = thetagg + 360;
    end
    theta = [theta,thetagg];
    reldist = [reldist,rgg];
    x_answer = [x_answer,centerx];
    y_answer = [y_answer,centery];
    
    % Define the distances between the simulated Tx and the different
    % antennas:
    if centerx > 0
        right = centerx - (lambda/2);
        dist = sqrt(right^2 + centery^2);
        d = [d,dist];
        rightright = centerx - lambda;
        dist = sqrt(rightright^2 + centery^2);
        d = [d,dist];
        left = centerx + (lambda/2);
        dist = sqrt(left^2 + centery^2);
        d = [d,dist];
        leftleft = centerx + lambda;
        dist = sqrt(leftleft^2 + centery^2);
        d = [d,dist];
    elseif centerx < 0
        right = (-1*centerx) + (lambda)/2;
        dist = sqrt(right^2 + centery^2);
        d = [d,dist];
        rightright = (-1*centerx) + (lambda);
        dist = sqrt(rightright^2 + centery^2);
        d = [d,dist];
        left = (-1*centerx) - (lambda/2);
        dist = sqrt(left^2 + centery^2);
        d = [d,dist];
        leftleft = (-1*centerx) - lambda;
        dist = sqrt(leftleft^2 + centery^2);
        d = [d,dist];
    end
    
    % n = Number of walls between the Tx and Rx
    if (centerx > 1000) && (centery > 1000)
        n = 2;
        lf_o = 4 * n;
        lf = [lf,lf_o,lf_o,lf_o,lf_o];
    elseif (centerx < -1000) && (centery > 1000)
        n = 3;
        lf_o = 4 * n;
        lf = [lf,lf_o,lf_o,lf_o,lf_o];
    elseif (centerx > 1100) && (centery < 1000)
        n = 1;
        lf_o = 4 * n;
        lf = [lf,lf_o,lf_o,lf_o,lf_o];
    else
        n = 0;
        lf_o = 4 * n;
        lf = [lf,lf_o,lf_o,lf_o,lf_o];
    end
end
% Scaling from cm to meters
d = d / 100;
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

prx = ptx - total_loss; % Tx pwer - loss = Rx power
prx = 1000 * (10.^(prx./10)); % Convert from dBm to Watts
%pre_noise_prx = prx;

% Adding Noise:
% Below we add a realistic amount of white gaussian noise
nfl = .00001; % Noise floor low power in Watts ~ -50 dB
nfh = .0001; % Noise floor high power in Watts ~ -40 dB
noise_len = length(d);
noise = sqrt(v) * ((nfh-nfl).*rand(1,noise_len) + nfl);
prx = prx + noise;

% Phase Shift:
% Now lets calculate the phase shift due to distance
td = d ./ (3*10^8); % Time delay which equals distance/speed
ps = (360 * f) .* td; % Phase difference in degrees
% Define reference phase
cenphase = (360 * f) .* (reldist ./ (3*10^8));

% Relative phase difference:
% Here we are trying to find the phase difference relative to the reference
% signal. In our final project design we divide the reference signal as a
% complex number by the complex signals at the receivers prior to FFT
% processing to obtain the relative phase difference. The division of
% phasors results in a subtraction of phases.
relative_phase = [];
phasecount = 1;
for k=(1:length(cenphase))
    for u=(1:4)
        relphase = cenphase(k) - ps(phasecount);
        phasecount = phasecount + 1;
        relative_phase = [relative_phase,relphase];
    end
end
 
% Shaping the array in preperation for the Neural Network:
% We want a 10 column tensor with the first 8 consisting of inputs and the
% last two consisitng of (x,y) or (r,theta).
power_phase_len = length(x);
power_phase = reshape([prx;relative_phase], size(prx,1), []);
power_phase = reshape(power_phase,[8,power_phase_len]);
new_power_phase = ones(power_phase_len,10);
power_phase = power_phase.'; % Transpose array
for z=(1:power_phase_len)
    for p=(1:8)
        new_power_phase(z,p) = power_phase(z,p) .* new_power_phase(z,p);
    end
    new_power_phase(z,9) = r(z);
    new_power_phase(z,10) = theta(z);
    %new_power_phase(z,9) = x_answer(z);
    %new_power_phase(z,10) = y_answer(z);
end

% Lets write the new array of tensors to a CSV file:
csvwrite('JTC_w_added_noise_5AA.csv',new_power_phase)

%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
