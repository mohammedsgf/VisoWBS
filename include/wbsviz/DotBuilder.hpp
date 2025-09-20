#pragma once
#include <string>
#include "Model.hpp"

namespace wbsviz {

class DotBuilder {
public:
    explicit DotBuilder(std::string rankdir = "TB");
    std::string build(const Tree& t) const;
private:
    std::string rankdir_;
    void emitNode(std::ostringstream& os, const Node* n) const;
    static std::string statusFill(const std::string& s);
};

} // namespace wbsviz
