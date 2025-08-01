import { useState } from "react";
import CircularText from "./components/CircularText";
import CurvedLoop from "./components/CurvedLoop";
import BitButton from "./components/ui/8bit/button";
import BitCard from "./components/ui/8bit/card";
import BitLabel from "./components/ui/8bit/label";
import BitInput from "./components/ui/8bit/input";
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "./components/ui/8bit/accordion"; // Import Accordion component
import "./App.css";

const STATUS_ICON = {
  Analyzing: "⏳",
  Analyzed: "✅",
  Failed: "❌",
};

function randomConfidence() {
  // 80~99 high, 60~79 medium, 40~59 low
  const r = Math.random();
  if (r > 0.7) return Math.floor(80 + Math.random() * 20);
  if (r > 0.3) return Math.floor(60 + Math.random() * 20);
  return Math.floor(40 + Math.random() * 20);
}

export default function App() {
  const [input, setInput] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");

  // Simulate analysis
  const handleAnalyze = () => {
    setLoading(true);
    setResults(
      input
        .split(/\s|,|;/)
        .filter(Boolean)
        .map((id) => ({
          id,
          status: "Analyzing",
          confidence: null,
          chain: "",
          spotCheck: false,
        }))
    );
    setTimeout(() => {
      setResults((prev) =>
        prev.map((r) => {
          // 10% fail
          if (Math.random() < 0.1) {
            return { ...r, status: "Failed", confidence: 0, chain: "Analysis failed." };
          }
          const conf = randomConfidence();
          return {
            ...r,
            status: "Analyzed",
            confidence: conf,
            chain: `Call chain for ${r.id}...`,
          };
        })
      );
      setLoading(false);
    }, 1500);
  };

  const handleRetry = (id) => {
    setResults((prev) =>
      prev.map((r) =>
        r.id === id
          ? { ...r, status: "Analyzing", confidence: null, chain: "" }
          : r
      )
    );
    setTimeout(() => {
      setResults((prev) =>
        prev.map((r) => {
          if (r.id !== id) return r;
          if (Math.random() < 0.1) {
            return { ...r, status: "Failed", confidence: 0, chain: "Analysis failed." };
          }
          const conf = randomConfidence();
          return {
            ...r,
            status: "Analyzed",
            confidence: conf,
            chain: `Call chain for ${r.id}...`,
          };
        })
      );
    }, 1200);
  };

  const handleSpotCheck = (id) => {
    setResults((prev) =>
      prev.map((r) =>
        r.id === id ? { ...r, spotCheck: !r.spotCheck } : r
      )
    );
  };

  const handleExport = (type) => {
    let data = results;
    if (filter !== "all") {
      data = data.filter((r) =>
        filter === "failed"
          ? r.status === "Failed"
          : filter === "low"
          ? r.confidence !== null && r.confidence < 60
          : filter === "spot"
          ? r.spotCheck
          : true
      );
    }
    if (type === "json") {
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "silver_results.json";
      a.click();
      URL.revokeObjectURL(url);
    } else {
      // txt
      const txt = data
        .map(
          (r) =>
            `${r.id}\t${r.status}\tConfidence: ${r.confidence ?? "-"}\n${r.chain}\n---\n`
        )
        .join("");
      const blob = new Blob([txt], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "silver_results.txt";
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  const filteredResults = results.filter((r) => {
    if (filter === "all") return true;
    if (filter === "failed") return r.status === "Failed";
    if (filter === "low") return r.confidence !== null && r.confidence < 60;
    if (filter === "spot") return r.spotCheck;
    return true;
  }).filter((r) => {
    if (!searchTerm) return true;
    return r.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
           r.chain.toLowerCase().includes(searchTerm.toLowerCase());
  });

  return (
    <div className="app-root">
      <div className="header-section">
        <CircularText text="SILVER - RustSec Analyzer" spinDuration={18} onHover="speedUp" />
        <CurvedLoop marqueeText="Automated Call Chain Visualization • LLM + Static Analysis • High Confidence • 8bit UI" speed={1.5} />
        <p className="description-text">
          Silver is an automated security analysis tool for RustSec IDs.
          It combines large language models (LLM) and static analysis to provide high-confidence call chain visualization.
          Simply input RustSec IDs to quickly understand their potential impact and call paths.
        </p>
      </div>
      
      <BitCard className="input-section">
        <BitLabel className="input-label">
          Input RustSec IDs (separated by commas, spaces, or line breaks):
        </BitLabel>
        <textarea
          id="rustsec-input"
          className="rustsec-input"
          rows={3}
          placeholder="Example: RUSTSEC-2022-0001, RUSTSEC-2023-0010"
          value={input}
          onChange={e => setInput(e.target.value)}
        />
        <div className="button-group">
          <BitButton
            onClick={handleAnalyze}
            disabled={loading || !input.trim()}
            style={{ marginTop: 16 }}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </BitButton>
          <BitButton
            onClick={() => setInput("")}
            disabled={!input.trim()}
            style={{ marginTop: 16, marginLeft: 8 }}
            variant="secondary"
          >
            Clear
          </BitButton>
        </div>
      </BitCard>

      <Accordion type="single" collapsible className="info-accordion">
        <AccordionItem value="item-1">
          <AccordionTrigger>What is Silver?</AccordionTrigger>
          <AccordionContent>
            Silver is a powerful security analysis tool specifically designed for automated analysis of RustSec IDs.
            It leverages advanced LLM and static analysis technologies to provide developers with clear, accurate call chain visualization,
            helping you quickly identify and understand potential security vulnerabilities.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-2">
          <AccordionTrigger>How to use?</AccordionTrigger>
          <AccordionContent>
            Paste one or more RustSec IDs in the input box above (supports comma, space, or line break separation),
            then click the "Analyze" button. The system will automatically analyze and display results, including confidence levels and call chain details.
            You can also filter and export the results.
          </AccordionContent>
        </AccordionItem>
      </Accordion>
      
      <BitCard className="results-section">
        <div className="results-toolbar">
          <div className="toolbar-left">
            <BitLabel>Filter:</BitLabel>
            <select value={filter} onChange={e => setFilter(e.target.value)} className="results-filter">
              <option value="all">All</option>
              <option value="failed">Failed</option>
              <option value="low">Low Confidence</option>
              <option value="spot">Spot Check</option>
            </select>
          </div>
          <div className="toolbar-right">
            <BitInput
              placeholder="Search results..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              style={{ width: "200px", marginRight: 8 }}
            />
            <BitButton onClick={() => handleExport("json")} size="sm">Export JSON</BitButton>
            <BitButton onClick={() => handleExport("txt")} size="sm" style={{ marginLeft: 8 }}>Export TXT</BitButton>
          </div>
        </div>
        
        <h2>Analysis Results ({filteredResults.length})</h2>
        {filteredResults.length === 0 && <div className="empty-tip">No results yet. Please input RustSec IDs and click analyze.</div>}
        
        <div className="results-grid">
          {filteredResults.map(r => (
            <BitCard key={r.id} className={`result-item ${r.status === "Failed" ? "failed" : r.confidence !== null && r.confidence < 60 ? "low-confidence" : ""}`}>
              <div className="result-row">
                <span className="status-icon">{STATUS_ICON[r.status] || ""}</span>
                <strong>{r.id}</strong>
                <span className="confidence-score">
                  {r.confidence !== null && r.status !== "Failed" ? `Confidence: ${r.confidence}` : null}
                </span>
              </div>
              <div className="call-chain">{r.chain}</div>
              {r.confidence !== null && r.confidence < 60 && r.status !== "Failed" && (
                <div className="confidence-warning">Low confidence, manual review required.</div>
              )}
              <div className="result-actions">
                {r.status === "Failed" && (
                  <BitButton onClick={() => handleRetry(r.id)} font="retro" size="sm">Retry</BitButton>
                )}
                <BitButton
                  onClick={() => handleSpotCheck(r.id)}
                  font="retro"
                  size="sm"
                  style={{ marginLeft: 8, background: r.spotCheck ? "#ffe066" : undefined }}
                >
                  {r.spotCheck ? "Spot Checked" : "Spot Check"}
                </BitButton>
              </div>
            </BitCard>
          ))}
        </div>
      </BitCard>
    </div>
  );
}
