#include "wbsviz/DotBuilder.hpp"
#include "wbsviz/Common.hpp"
#include <sstream>
#include <vector>

namespace wbsviz {

DotBuilder::DotBuilder(std::string rankdir) : rankdir_(std::move(rankdir)) {}

int DotBuilder::levelOf(const std::string& code) {
    if (code.empty()) return 0;
    int dots = 0;
    for (char c : code) if (c == '.') ++dots;
    return dots + 1;
}

// Soft, readable palette (cycles after L8)
static const char* kLevelPalette[] = {
    "#E3F2FD", // L1  blue-50
    "#E8F5E9", // L2  green-50
    "#FFF3E0", // L3  orange-50
    "#F3E5F5", // L4  purple-50
    "#FCE4EC", // L5  pink-50
    "#E0F2F1", // L6  teal-50
    "#FFFDE7", // L7  yellow-50
    "#ECEFF1"  // L8  blue-grey-50
};

std::string DotBuilder::fillByLevel(const std::string& code) {
    int lvl = levelOf(code);
    if (lvl <= 0) return "#FFFFFF";
    size_t idx = static_cast<size_t>((lvl - 1) % (sizeof(kLevelPalette)/sizeof(kLevelPalette[0])));
    return kLevelPalette[idx];
}

void DotBuilder::emitNode(std::ostringstream& os, const Node* n) const {
    // First line: code + title
    std::ostringstream label;
    label << esc(n->code) << "  " << esc(n->title);

    // Second line: compact metadata (optional fields shown if present)
    std::vector<std::string> parts;
    if (!n->primaryResp.empty())   parts.push_back("PR: " + esc(n->primaryResp));
    if (!n->seconderyResp.empty()) parts.push_back("SR: " + esc(n->seconderyResp));
    if (!n->estimateDuration.empty()) parts.push_back("Est: " + esc(n->estimateDuration));

    if (!parts.empty()) {
        label << "\\n(";
        for (size_t i=0;i<parts.size();++i) {
            if (i) label << " | ";
            label << parts[i];
        }
        label << ")";
    }

    const std::string fill = fillByLevel(n->code);

    // Tooltip uses the (possibly long) description
    std::string tooltip = esc(n->description);

    os << "  \"" << esc(n->code) << "\""
       << " [label=\"" << label.str() << "\","
       << " style=\"filled\", shape=box, fontsize=10, margin=\"0.06,0.04\","
       << " penwidth=1.0, fillcolor=\"" << fill << "\","
       << " tooltip=\"" << tooltip << "\","
       << " URL=\"#\", target=\"_top\""   // forces <a>… -> pointer cursor
       << "];\n";

    // // --- enforce sibling order on the same rank ---
    // if (n->children.size() > 1) {
    //     // keep all siblings on the same rank
    //     os << "  { rank=same; ";
    //     for (auto* c : n->children) os << "\"" << esc(c->code) << "\"; ";
    //     os << "}\n";
    //     // invisible chain to preserve left→right order
    //     for (size_t i = 1; i < n->children.size(); ++i) {
    //         os << "  \"" << esc(n->children[i-1]->code) << "\" -> \"" << esc(n->children[i]->code)
    //            << "\" [style=invis, weight=100];\n";
    //     }
    // }

    for (auto* c : n->children) {
        os << "  \"" << esc(n->code) << "\" -> \"" << esc(c->code) << "\" [arrowhead=none];\n";
        emitNode(os, c);
    }
}

std::string DotBuilder::build(const Tree& t) const {
    std::ostringstream os;
    // os << "digraph WBS {\n"
    //       "  graph [rankdir=" << (rankdir_=="LR"?"LR":"TB") << ", nodesep=0.4, ranksep=0.7];\n"
    //       "  node  [shape=box, style=filled, fontsize=10];\n";
    os << "digraph WBS {\n"
   << "  graph [rankdir=" << (rankdir_=="LR"?"LR":"TB")
   << ", nodesep=0.6, ranksep=0.9, splines=ortho, ordering=out, outputorder=edgesfirst];\n"
   << "  edge  [arrowhead=none, weight=3, tailport=s, headport=n, minlen=1];\n"
   << "  node  [shape=box, style=rounded, fontsize=10];\n";
    for (auto* r : t.roots) emitNode(os, r);
    os << "}\n";
    return os.str();
}

} // namespace wbsviz
