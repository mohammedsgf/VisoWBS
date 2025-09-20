#include "wbsviz/DotBuilder.hpp"
#include "wbsviz/Common.hpp"
#include <sstream>

namespace wbsviz {

DotBuilder::DotBuilder(std::string rankdir) : rankdir_(std::move(rankdir)) {}

std::string DotBuilder::statusFill(const std::string& s0){
    auto s=toLower(s0);
    if (s=="done"||s=="completed") return "#E6F4EA";
    if (s=="in-progress"||s=="wip") return "#E8F0FE";
    if (s=="blocked"||s=="issue"||s=="risk") return "#FEEEEE";
    if (s=="on-hold"||s=="paused") return "#FFF8E1";
    return "#FFFFFF";
}

void DotBuilder::emitNode(std::ostringstream& os, const Node* n) const {
    std::ostringstream label;
    label << esc(n->code) << "  " << esc(n->title);
    if (!n->owner.empty() || !n->status.empty()) {
        label << "\\n(" << esc(n->owner);
        if (!n->owner.empty() && !n->status.empty()) label << " | ";
        label << esc(n->status) << ")";
    }
    os << "  \"" << esc(n->code) << "\""
       << " [label=\"" << label.str() << "\", style=\"rounded,filled\", fillcolor=\"" << statusFill(n->status)
       << "\", margin=\"0.06,0.04\", penwidth=1.0, fontsize=10];\n";
    for (auto* c : n->children) {
        os << "  \"" << esc(n->code) << "\" -> \"" << esc(c->code) << "\" [arrowhead=none];\n";
        emitNode(os, c);
    }
}

std::string DotBuilder::build(const Tree& t) const {
    std::ostringstream os;
    os << "digraph WBS {\n"
          "  graph [rankdir=" << (rankdir_=="LR"?"LR":"TB") << ", nodesep=0.4, ranksep=0.7];\n"
          "  node  [shape=box, style=rounded, fontsize=10];\n";
    for (auto* r : t.roots) emitNode(os, r);
    os << "}\n";
    return os.str();
}

} // namespace wbsviz
