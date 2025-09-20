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
    static std::string fillByLevel(const std::string& code);
    static int levelOf(const std::string& code); // 1 for "1", 2 for "1.1", ...
};

} // namespace wbsviz
