use walkdir::WalkDir;
use syn::{visit::Visit, ItemFn, ExprCall, spanned::Spanned};
use std::fs;
use std::collections::{HashSet, HashMap};

/// 递归提取真实调用链，返回 txt 格式
pub fn extract_call_chain_real(project_path: &str, entry_fn: &str) -> String {
    // 1. 遍历所有 .rs 文件，收集函数定义和调用关系
    let mut fn_map: HashMap<String, Vec<String>> = HashMap::new();
    let mut fn_bodies: HashMap<String, String> = HashMap::new();
    for entry in WalkDir::new(project_path).into_iter().filter_map(|e| e.ok()) {
        if entry.path().extension().map(|s| s == "rs").unwrap_or(false) {
            if let Ok(src) = fs::read_to_string(entry.path()) {
                if let Ok(ast) = syn::parse_file(&src) {
                    let mut visitor = FnCallVisitor::new();
                    visitor.visit_file(&ast);
                    for (name, calls) in visitor.calls {
                        fn_map.entry(name.clone()).or_default().extend(calls);
                    }
                    for (name, body) in visitor.bodies {
                        fn_bodies.insert(name, body);
                    }
                }
            }
        }
    }
    // 2. 递归生成调用链
    let mut visited = HashSet::new();
    let mut lines = vec![];
    build_chain(entry_fn, &fn_map, &fn_bodies, 0, &mut visited, &mut lines);
    lines.join("\n")
}

/// 递归提取真实调用链，返回 Mermaid flowchart 格式
pub fn extract_call_chain_mermaid_real(project_path: &str, entry_fn: &str) -> String {
    let mut fn_map: HashMap<String, Vec<String>> = HashMap::new();
    for entry in WalkDir::new(project_path).into_iter().filter_map(|e| e.ok()) {
        if entry.path().extension().map(|s| s == "rs").unwrap_or(false) {
            if let Ok(src) = fs::read_to_string(entry.path()) {
                if let Ok(ast) = syn::parse_file(&src) {
                    let mut visitor = FnCallVisitor::new();
                    visitor.visit_file(&ast);
                    for (name, calls) in visitor.calls {
                        fn_map.entry(name.clone()).or_default().extend(calls);
                    }
                }
            }
        }
    }
    let mut visited = HashSet::new();
    let mut lines = vec!["graph TD".to_string()];
    build_mermaid_chain(entry_fn, &fn_map, &mut visited, &mut lines);
    lines.join("\n")
}

struct FnCallVisitor {
    calls: HashMap<String, Vec<String>>,
    bodies: HashMap<String, String>,
    current_fn: Option<String>,
}

impl FnCallVisitor {
    fn new() -> Self {
        Self { calls: HashMap::new(), bodies: HashMap::new(), current_fn: None }
    }
}

impl<'ast> Visit<'ast> for FnCallVisitor {
    fn visit_item_fn(&mut self, i: &'ast ItemFn) {
        let name = i.sig.ident.to_string();
        self.current_fn = Some(name.clone());
        // 保存函数体源码片段
        let span = i.block.span();
        let body = format!("{}", quote::quote! { #i });
        self.bodies.insert(name.clone(), body);
        syn::visit::visit_item_fn(self, i);
        self.current_fn = None;
    }
    fn visit_expr_call(&mut self, node: &'ast ExprCall) {
        if let Some(cur) = &self.current_fn {
            if let syn::Expr::Path(ref path) = *node.func {
                let called = path.path.segments.last().unwrap().ident.to_string();
                self.calls.entry(cur.clone()).or_default().push(called);
            }
        }
        syn::visit::visit_expr_call(self, node);
    }
}

fn build_chain(
    fn_name: &str,
    fn_map: &HashMap<String, Vec<String>>,
    fn_bodies: &HashMap<String, String>,
    depth: usize,
    visited: &mut HashSet<String>,
    lines: &mut Vec<String>,
) {
    if !visited.insert(fn_name.to_string()) { return; }
    let indent = "  ".repeat(depth);
    lines.push(format!("{}{}()", indent, fn_name));
    if let Some(calls) = fn_map.get(fn_name) {
        for callee in calls {
            lines.push(format!("{}→ {}()", indent, callee));
            build_chain(callee, fn_map, fn_bodies, depth+1, visited, lines);
        }
    }
}

fn build_mermaid_chain(
    fn_name: &str,
    fn_map: &HashMap<String, Vec<String>>,
    visited: &mut HashSet<String>,
    lines: &mut Vec<String>,
) {
    if !visited.insert(fn_name.to_string()) { return; }
    if let Some(calls) = fn_map.get(fn_name) {
        for callee in calls {
            lines.push(format!("{}[{}] --> {}[{}]", fn_name, fn_name, callee, callee));
            build_mermaid_chain(callee, fn_map, visited, lines);
        }
    }
}

/// 分析项目并返回调用链
pub fn analyze_project(project_path: &str, test_hash: Option<&str>) -> String {
    let entry_fn = test_hash.unwrap_or("main");
    extract_call_chain_real(project_path, entry_fn)
} 