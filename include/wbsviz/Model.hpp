#pragma once
#include <string>
#include <vector>
#include <memory>
#include <unordered_map>

namespace wbsviz {

struct Record {
    std::string code, title, owner, status, start, end, estimate;
};

struct Node {
    std::string code, title, owner, status, start, end, estimate;
    std::vector<Node*> children;
};

struct Tree {
    std::unordered_map<std::string,std::unique_ptr<Node>> store;
    std::vector<Node*> roots;
};

} // namespace wbsviz
