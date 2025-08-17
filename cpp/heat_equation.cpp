#include <stdlib.h>
#include <vector>

#define data_type float

std::vector<data_type> time_setp(const std::vector<data_type> &temperature,
                                 const data_type diffusion_const) {

    // Creating new temperature vector.
    std::vector<data_type> new_temperature(temperature.size());
    
    // Iterate through the temperatures ignoring the values on the boundary.
    for (int i = 1; i < temperature.size() - 1; ++i) {
        new_temperature[i] = temperature[i] + diffusion_const * (temperature[i+1] + temperature[i-1] - 2 * temperature[i]);
    }

    return new_temperature;
}
