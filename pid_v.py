import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class pid(object):
    '''
    A very simple PID class.
    '''
    def __init__(self, p, i_t, d_t, loss=-10.):
        '''
        p (float): proportional coefficient.
        i_t (float): integral time.
        d_t (float): derivative time.
        All p, i, and d must be positive.
        loss (float): loss constant, must be negative.
        '''
        if p < 0.0 or i_t < 0.0 or d_t < 0.0:
            raise ValueError("p, i, and d must be positive")
        if loss >=0:
            raise ValueError("loss must be negative")
        self.p_gain = p
        self.i_time = i_t
        self.d_time = d_t
        self.loss = loss
        # link the coefficients
        self.i_gain = p / i_t
        self.d_gain = p * d_t
    
    def run(self, sp_i=50, run_t=200, ramp=0):
        '''
        Simulate a simple PID heating run, assuming the lowest temperature is 0.
        sp_i (float): initial setpoint temperature.
        run_t (int): running time in seconds.
        ramp (float): ramp rate in degrees per second.
        '''
        if run_t <= 0:
            raise ValueError("time must be positive")
        if sp_i < 0 or ramp < 0:
            raise ValueError("setpoint and ramp must be positive (heating only)")
        self.time_range = np.arange(run_t)
        # current setpoint = initial setpoint + ramp * time
        self.sp_range = np.array([sp_i+t*ramp for t in self.time_range])
        # initialize the measured temperature, error, and outputs
        self.measured = [0]
        error_i = sp_i - self.measured[0]
        self.errors = [error_i]
        p_o = self.p_gain * error_i
        i_o = self.i_gain * np.sum(self.errors)
        d_o = 0
        outputs = np.max((p_o + i_o + d_o, 0))
        measure_i = self.measured[0] + outputs + self.loss
        self.measured.append(measure_i)
        for i, sp in enumerate(self.sp_range[1:-1], 1):
            error_i = sp - self.measured[i]
            self.errors.append(error_i)
            p_o = self.p_gain * error_i
            i_o = self.i_gain * np.sum(self.errors)
            d_o = self.d_gain * (self.errors[i] - self.errors[i-1])
            outputs = np.max((p_o + i_o + d_o, 0))
            measure_i = np.max((self.measured[i] + outputs + self.loss, 0))
            self.measured.append(measure_i)
    
    def update(self, p, i_t, d_t, loss, sp_i=50, run_t=200, ramp=0):
        '''
        Update the parameters and run again.
        p (float): proportional coefficient.
        i_t (float): integral time.
        d_t (float): derivative time.
        All p, i, and d must be positive.
        loss (float): loss constant, must be negative.
        sp_i (float): initial setpoint temperature.
        run_t (int): running time in seconds.
        ramp (float): ramp rate in degrees per second.
        '''
        if p < 0.0 or i_t < 0.0 or d_t < 0.0:
            raise ValueError("p, i, and d must be positive")
        if loss >=0:
            raise ValueError("loss must be negative")
        # update the parameters
        self.p_gain = p
        self.i_time = i_t
        self.d_time = d_t
        self.loss = loss
        self.i_gain = p / i_t
        self.d_gain = p * d_t
        # run again
        self.run(sp_i=sp_i, run_t=run_t, ramp=ramp)

if __name__ == '__main__':
    pid_1 = pid(10.0, 10.0, 2.0)
    pid_1.run(50, 200, 10)