#pragma once
#include <vector>
#include "Model.hpp"

namespace wbsviz {

class TreeBuilder {
public:
    explicit TreeBuilder(bool strict);
    Tree build(const std::vector<Record>& recs);
private:
    bool strict_;
};

} // namespace wbsviz
