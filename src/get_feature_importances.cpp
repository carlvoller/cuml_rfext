#include <iostream>
#include <vector>
#include <climits>
#include <cuml/ensemble/randomforest.hpp> // Include cuML/RAFT utilities
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#define PYBIND11_DETAILED_ERROR_MESSAGES

namespace py = pybind11;
using namespace ML;

template <typename T>
T sum(py::array_t<T> arr)
{
    int num_of_elements = arr.size();
    auto arr_ref = arr.unchecked();
    T total_sum = 0;
    for (int i = 0; i < num_of_elements; i++)
    {
        total_sum += arr_ref(i);
    }
    // py::print("a sum is", total_sum);
    return total_sum;
}

template <typename T>
py::array_t<T> get_tree_feature_importances(
    std::shared_ptr<DT::TreeMetaDataNode<T, T>> tree,
    int n_features,
    bool normalize)
{

    std::vector<SparseTreeNode<T, T>> branches = tree->sparsetree;
    int no_of_nodes = branches.size() & INT_MAX;

    // Create importances
    py::array_t<T> importances = py::array_t<T>({n_features});
    importances[py::make_tuple(py::ellipsis())] = 0.0;

    if (no_of_nodes > 1)
    {

        auto importances_mut = importances.mutable_unchecked();

        for (int x = 0; x < no_of_nodes; x++)
        {
            SparseTreeNode<T, T> *Node = &branches[x];
            if (Node->LeftChildId() != -1)
            {
                importances_mut(Node->ColumnId()) += Node->BestMetric();
            }
        }

        if (normalize)
        {
            T total_sum = sum(importances);
            if (total_sum > 0.0)
            {
                for (int x = 0; x < n_features; x++)
                {
                    importances_mut(x) /= total_sum;
                }
            }
        }
    }

    return importances;
}

template <typename T>
py::array_t<T> compute_feature_importances(RandomForestMetaData<T, T> *rf_forest, int n_features)
{

    RF_params rf_params = rf_forest->rf_params;

    std::vector<py::array_t<T>> all_importances;

    for (int i = 0; i < rf_params.n_trees; i++)
    {
        std::shared_ptr<DT::TreeMetaDataNode<T, T>> tree = rf_forest->trees[i];
        // if (tree->leaf_counter > 1) {
        py::array_t<T> importances = get_tree_feature_importances<T>(tree, n_features, false);
        all_importances.push_back(importances);
        // }
    }

    if (all_importances.size() == 0)
    {
        py::array_t<T> arr = py::array_t<T>({n_features});
        arr[py::make_tuple(py::ellipsis())] = 0.0;
        return arr;
    }

    int num_of_importances = (int)all_importances.size();

    py::array_t<T> final_importances = py::array_t<T>({n_features});
    final_importances[py::make_tuple(py::ellipsis())] = 0.0;
    auto final_importances_mut = final_importances.mutable_unchecked();

    for (int i = 0; i < num_of_importances; i++)
    {
        py::array_t<T> current_importances = all_importances[i];
        auto current_importances_ref = current_importances.unchecked();

        for (int j = 0; j < n_features; j++)
        {
            T value = current_importances_ref(j);
            final_importances_mut(j) += value;
        }
    }

    for (int i = 0; i < n_features; i++)
    {
        final_importances_mut(i) /= num_of_importances;
    }

    T sum_of_mean = sum(final_importances);

    for (int i = 0; i < n_features; i++)
    {
        final_importances_mut(i) /= sum_of_mean;
    }

    return final_importances;
}

int main()
{
    printf("%s", "hello world");
    return 0;
}