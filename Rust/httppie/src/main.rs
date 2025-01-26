use anyhow::Result;
use clap::{Parser, Subcommand};
use reqwest::{header, Client, Response};
use std::str::FromStr;

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
    #[arg(value_name = "KEY=VALUE", value_parser=parse_kv_pair)] //  更新了 #[arg] 的用法
    body: Vec<KvPair>,
}

/// 命令行中的 key=value 可以通过 parse_kv_pair 解析成 KvPair 结构
#[derive(Debug, Clone)]
struct KvPair {
    key: String,
    value: String,
}

impl FromStr for KvPair {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // 使用 = 进行 split，这会得到一个迭代器
        let mut split = s.split("=");
        let key = split.next().ok_or("missing key")?;
        let value = split.next().ok_or("missing value")?;
        if split.next().is_some() {
            return Err("invalid key=value".to_string());
        }
        Ok(KvPair {
            key: key.to_string(),
            value: value.to_string(),
        })
    }
}

/// 因为我们为 KvPair 实现了 FromStr，这里可以直接 s.parse() 得到 KvPair
fn parse_kv_pair(s: &str) -> Result<KvPair, String> {
    s.parse()
}

async fn get(client: Client, args: &Get) -> Result<()> {
    let resp = client.get(&args.url).send().await?;
    println!("{:?}", resp.text().await?);
    Ok(())
}

async fn post(client: Client, args: &Post) -> Result<()> {
    let mut body = std::collections::HashMap::new();
    for pair in args.body.iter() {
        body.insert(&pair.key, &pair.value);
    }
    let resp = client.post(&args.url).json(&body).send().await?;
    println!("{:?}", resp.text().await?);
    Ok(())
}

#[tokio::main]
async fn main() -> Result<()> {
    let opts: Opts = Opts::parse();
    let client = Client::new();
    let result = match opts.subcmd {
        SubCommand::Get(ref args) => get(client, args).await?,
        SubCommand::Post(ref args) => post(client, args).await?,
    };

    Ok(result)
}
