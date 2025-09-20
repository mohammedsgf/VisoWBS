#include "wbsviz/TreeBuilder.hpp"
#include "wbsviz/Common.hpp"
#include <algorithm>
#include <sstream>
#include <stdexcept>
#include <functional>

namespace wbsviz {

TreeBuilder::TreeBuilder(bool strict) : strict_(strict) {}

Tree TreeBuilder::build(const std::vector<Record>& recs) {
    Tree t;

    // Create nodes & validate
    for (const auto& r: recs) {
        if (!validCode(r.code)) throw std::runtime_error("Invalid code: " + r.code);
        if (t.store.count(r.code)) throw std::runtime_error("Duplicate code: " + r.code);
        auto n = std::make_unique<Node>();
        n->code = r.code;
        n->title = r.title;
        n->description = r.description;
        n->primaryResp = r.primaryResp;
        n->seconderyResp = r.seconderyResp;
        n->estimateDuration = r.estimateDuration;
        t.store[r.code] = std::move(n);
    }

    // Ensure parents exist (auto-create if !strict_)
    std::function<void(const std::string&)> ensureParent = [&](const std::string& code){
        if (code.empty()) return;
        if (!t.store.count(code)) {
            if (strict_) throw std::runtime_error("Missing parent: " + code);
            auto p = std::make_unique<Node>();
            p->code = code; p->title = "[Auto] " + code;
            t.store[code] = std::move(p);
            ensureParent(parentCode(code));
        }
    };
    for (const auto& kv : t.store) ensureParent(parentCode(kv.first));

    // Link children & roots
    for (auto& kv : t.store) {
        Node* n = kv.second.get();
        auto p = parentCode(n->code);
        if (p.empty()) t.roots.push_back(n);
        else t.store[p]->children.push_back(n);
    }

    // Sort by numeric code segments
    auto codeLess = [](const Node* a, const Node* b){
        auto split = [](const std::string& s){ std::vector<int> v; std::stringstream ss(s); std::string tok; while(std::getline(ss,tok,'.')) v.push_back(std::stoi(tok)); return v; };
        auto va=split(a->code), vb=split(b->code);
        size_t N=std::min(va.size(),vb.size());
        for(size_t i=0;i<N;++i) if (va[i]!=vb[i]) return va[i]<vb[i];
        return va.size()<vb.size();
    };
    for (auto& kv : t.store) std::sort(kv.second->children.begin(), kv.second->children.end(), codeLess);
    std::sort(t.roots.begin(), t.roots.end(), codeLess);

    return t;
}

} // namespace wbsviz
