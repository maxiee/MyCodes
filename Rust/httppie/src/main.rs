use clap::{Parser, Subcommand};

/// A naive httpie implementation with Rust, can you imagine how easy it is?
#[derive(Parser, Debug)]
#[command(
    author = "Maxiee",
    version = "1.0",
    about = "A naive httpie implementation with Rust"
)]
#[command(propagate_version = true)] // 建议加上，使子命令也能继承版本信息
struct Opts {
    #[command(subcommand)]
    subcmd: SubCommand,
}

#[derive(Subcommand, Debug)]
enum SubCommand {
    Get(Get),
    Post(Post),
}

/// feed get with an url and we will retrieve the response for you
#[derive(Parser, Debug)] // 子命令的结构体也需要使用 #[derive(Parser)] 或 #[derive(Args)]，这里作为子命令入口用 Parser
struct Get {
    /// HTTP 请求的 URL
    #[arg(value_name = "URL", value_parser = parse_url)]
    // 使用 #[arg] 替代 #[clap]，并使用 value_name 设置帮助信息中的名称
    url: String,
}

fn parse_url(s: &str) -> Result<String, String> {
    if s.starts_with("http://") || s.starts_with("https://") {
        Ok(s.to_string())
    } else {
        Err("URL must start with http:// or https://".to_string())
    }
}

/// feed post with an url and optional key=value pairs. We will post the data
/// as JSON, and retrieve the response for you
#[derive(Parser, Debug)] // 子命令的结构体也需要使用 #[derive(Parser)]
struct Post {
    /// HTTP 请求的 URL
    #[arg(value_name = "URL")]
    url: String,
    /// HTTP 请求的 body，可以多次输入 key=value
    #[arg(value_name = "KEY=VALUE")] //  更新了 #[arg] 的用法
    body: Vec<String>,
}

fn main() {
    let opts: Opts = Opts::parse(); // 使用 Opts::parse() 而不是 Clap::parse()
    println!("{:?}", opts);
}
