

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cassert>
#include <cmath>
#include <stdexcept>

/*for the namespace let us reduce it*/

namespace py = pybind11;

py::array_t<float> fusion(py::array_t<float>tab_a,py::array_t<float>tab_b,float w,float thresh){


     /*request the memory space where we stored our numpy array a and b */
    auto buf_a = tab_a.request();
    auto buf_b = tab_b.request();

    if(buf_a.size == 0 || buf_b.size == 0){
        throw std::runtime_error("Arrays are not to be empty !\n");
    }

    if(buf_a.size != buf_b.size){
        throw std::runtime_error("Buffers not of equal size\n");
    }

    /*let us verify the float variables w and thresh(threshold)*/

    if(!std::isfinite(w) || !std::isfinite(thresh)){
        throw std::runtime_error("w and thresh must be finite float!\n");
    }
    if(w < 0.0f || w > 1.0f){
        throw std::runtime_error("w's value must be in [0,1]\n");
    }
    if(thresh < 0.0f){
     throw std::runtime_error("Threshold cannot be below 0\n");
    }


    /*now in a same space to combine for our late fusion, text and tabular data must not necesserally belong to the same space
    however their set must be of equal size ex: R_text = 200 and R_tabular = 200 otherwise can't carry out any test*/
       if(buf_a.ndim != 1 || buf_b.ndim != 1){
        throw std::runtime_error("Your inputs must be of dim 1D\n");
      }

    //no null ptr thus format checking
    if(!buf_a.ptr || !buf_b.ptr) throw std::runtime_error("null pointers are not allowed\n");
    if ((buf_a.format != py::format_descriptor<float>::format()) ||
    (buf_b.format != py::format_descriptor<float>::format())) 
        {
            throw std::runtime_error("error not float32\n");
        }
    //threw a cast to my void pointers to have float32 buffers
    float* a = static_cast<float*>(buf_a.ptr);
    float* b = static_cast<float*>(buf_b.ptr);
    //allocation + memory access
    py::array_t<float>result(buf_a.size);
    auto buf_r = result.request();
    //casting to float to use my pointer to fill in the array
    float*r = static_cast<float*>(buf_r.ptr);

    //finally the calculation of our latefusion + w
    for(ssize_t i = 0; i< buf_a.size; ++i){
        float v = w * a[i] + (1.0f-w)*b[i];
        r[i] = (v > thresh) ? v : 0.0f;
    }
    return result;

}

PYBIND11_MODULE(late_fusion_cpp,m){
    m.def("fusion",&fusion);
}
