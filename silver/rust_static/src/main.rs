mod analyzer;
use clap::Parser;
use serde::Serialize;
use std::fs;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to the Rust project
    #[arg(short, long)]
    project_path: String,

    /// Test hash or entry function
    #[arg(short, long)]
    test_hash: Option<String>,

    /// Output file (json)
    #[arg(short, long)]
    output: Option<String>,
}

#[derive(Serialize)]
struct CallChainResult {
    status: String,
    call_chain: String,
    confidence: u8,
}

fn main() {
    let args = Args::parse();
    let result = analyzer::analyze_project(&args.project_path, args.test_hash.as_deref());
    let output = CallChainResult {
        status: "ok".to_string(),
        call_chain: result,
        confidence: 90,
    };
    let json = serde_json::to_string_pretty(&output).unwrap();
    if let Some(out_path) = args.output {
        fs::write(out_path, &json).expect("Failed to write output");
    } else {
        println!("{}", json);
    }
}
