#pragma once
#include <string>
#include <vector>
#include <memory>
#include <unordered_map>

namespace wbsviz {

struct Record {
    std::string code, title, description, primaryResp, seconderyResp, estimateDuration;
};

struct Node {
    std::string code, title, description, primaryResp, seconderyResp, estimateDuration;
    std::vector<Node*> children;
};

struct Tree {
    std::unordered_map<std::string,std::unique_ptr<Node>> store;
    std::vector<Node*> roots;
};

} // namespace wbsviz
