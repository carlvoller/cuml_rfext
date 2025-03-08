#include <iostream>
#include <vector>
#include <exception>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "get_feature_importances.cpp"

#define PYBIND11_DETAILED_ERROR_MESSAGES
#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

py::array_t<float> get_feature_importance_f(uintptr_t rf_forest_ptr, int n_features) {
    RandomForestMetaData<float, float> *rf_forest = (RandomForestMetaData<float, float>*)rf_forest_ptr;
    return compute_feature_importances(rf_forest, n_features);
}

py::array_t<double> get_feature_importance_d(uintptr_t rf_forest_ptr, int n_features) {
    RandomForestMetaData<double, double> *rf_forest = (RandomForestMetaData<double, double>*)rf_forest_ptr;
    return compute_feature_importances(rf_forest, n_features);
}

PYBIND11_MODULE(_core, m) {
    m.def("get_feature_importance_f", &get_feature_importance_f, "Calculates feature importances of the entire random forest (dtype=float32)");
    m.def("get_feature_importance_d", &get_feature_importance_d, "Calculates feature importances of the entire random forest (dtype=float64)");
    #ifdef VERSION_INFO
        m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
    #else
        m.attr("__version__") = "dev";
    #endif
}