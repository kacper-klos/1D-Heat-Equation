#include <stdlib.h>
#include <vector>
#include <cstdint>
#include <cmath>
#include <stdexcept>

#define data_type float

std::vector<data_type> time_step(const std::vector<data_type> &temperature,
                                 const data_type diffusion_const) {

    // Creating new temperature vector.
    std::vector<data_type> new_temperature(temperature.size());
    
    // Iterate through the temperatures ignoring the values on the boundary.
    for (int i = 1; i < temperature.size() - 1; ++i) {
        new_temperature[i] = temperature[i] + diffusion_const * (temperature[i+1] + temperature[i-1] - 2 * temperature[i]);
    }

    return new_temperature;
}

std::vector<std::vector<data_type>> simulate(const std::vector<data_type> &initial_conditions,
                                             const data_type diffusion_constant,
                                             const uint32_t frames_count) {
    // Create vector for frames
    std::vector<std::vector<data_type>> frames(frames_count+1);
    frames[0] = initial_conditions;

    // Fill frames with simulation predictions
    for (int i = 1; i < frames_count; ++i) {
        frames[i] = time_step(frames[i-1], diffusion_constant);
    }
    return frames;
}

std::vector<std::vector<data_type>> simulation_init(const std::vector<data_type> &initial_conditions,
                                                    const data_type time,
                                                    const data_type dt,
                                                    const data_type dx,
                                                    const data_type a) {
    // Analize input
    if (time < dt) {
        throw std::invalid_argument("Time must be greater or equal to dt");
    } else if (initial_conditions.size() < 3) {
        throw std::invalid_argument("Initial temperatures must have a size greater then 2");
    }

    // Calculate constanst
    data_type diffusion_const = a * dt / (dx * dx);
    uint32_t frames_count = std::ceil(time / dt);

    // Simulate
    return simulate(initial_conditions, diffusion_const, frames_count);
}
