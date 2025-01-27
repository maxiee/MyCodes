// 引入 protobuf 生成的代码，我们暂且不用太关心他们
mod engine;
mod pb;

use axum::{
    extract::Path,
    http::{HeaderMap, HeaderValue, StatusCode},
    routing::get,
    Extension, Router,
};
use bytes::Bytes;
use lru::LruCache;
use percent_encoding::{percent_decode_str, percent_encode, NON_ALPHANUMERIC};
use serde::Deserialize;
use std::{
    convert::TryInto,
    hash::{DefaultHasher, Hash, Hasher},
    net::SocketAddr,
    num::NonZero,
    sync::Arc,
};
use tokio::sync::Mutex;
use tracing::{info, instrument};

use engine::{Engine, Photon};
use image::ImageFormat as ImageOutputFormat;
use pb::*; // This is the newer way

// 参数使用 serde 做 Deserialize，axum 会自动识别并解析
#[derive(Deserialize)]
struct Params {
    spec: String,
    url: String,
}

type Cache = Arc<Mutex<LruCache<u64, Bytes>>>; // 一个线程安全的 LRU 缓存

#[tokio::main]
async fn main() {
    // 初始化 tracing
    tracing_subscriber::fmt::init();
    // 初始化缓存
    let cache: Cache = Arc::new(Mutex::new(LruCache::new(NonZero::new(1024).unwrap())));

    // 构建路由
    let app = Router::new()
        // `GET /image` 会执行 generate 函数，并把 spec 和 url 传递过去
        .route("/image/{spec}/{url}", get(generate))
        .layer(Extension(cache));

    // 运行 web 服务器
    let addr = "127.0.0.1:3000".parse::<SocketAddr>().unwrap();

    print_test_url("https://images.pexels.com/photos/1562477/pexels-photo-1562477.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=750&w=1260");

    info!("Listening on {}", addr);
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

// 目前我们就只把参数解析出来
async fn generate(
    Path(Params { spec, url }): Path<Params>,
    Extension(cache): Extension<Cache>,
) -> Result<(HeaderMap, Vec<u8>), StatusCode> {
    let url = percent_decode_str(&url).decode_utf8_lossy();
    let spec: ImageSpec = spec
        .as_str()
        .try_into()
        .map_err(|_| StatusCode::BAD_REQUEST)?;
    let url: &str = &percent_decode_str(&url).decode_utf8_lossy();

    let data = retrieve_image(&url, cache)
        .await
        .map_err(|_| StatusCode::BAD_REQUEST)?;

    let mut engine: Photon = data
        .try_into()
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    engine.apply(&spec.specs);

    let image = engine.generate(ImageOutputFormat::Jpeg);

    info!("Finished processing: image size {}", image.len());

    let mut headers = HeaderMap::new();
    headers.insert("content-type", HeaderValue::from_static("image/jpeg"));
    Ok((headers, image))
}

#[instrument(level = "info", skip(cache))]
async fn retrieve_image(url: &str, cache: Cache) -> Result<Bytes, reqwest::Error> {
    let mut hasher = DefaultHasher::new();
    url.hash(&mut hasher);
    let key = hasher.finish();

    // First try to get from cache
    if let Some(data) = cache.lock().await.get(&key) {
        info!("Cache hit: {}", key);
        return Ok(data.clone());
    }

    // If not in cache, retrieve from URL
    info!("Cache miss - retrieving from URL: {}", url);
    let resp = reqwest::get(url).await?;
    let data = resp.bytes().await?;

    // Store in cache
    cache.lock().await.put(key, data.clone());

    Ok(data)
}

// 调试辅助函数
fn print_test_url(url: &str) {
    use std::borrow::Borrow;
    let spec1 = Spec::new_resize(500, 800, resize::SampleFilter::CatmullRom);
    let spec2 = Spec::new_watermark(20, 20);
    let spec3 = Spec::new_filter(filter::Filter::Marine);
    let image_spec = ImageSpec::new(vec![spec1, spec2, spec3]);
    let s: String = image_spec.borrow().into();
    let test_image = percent_encode(url.as_bytes(), NON_ALPHANUMERIC).to_string();
    println!("test url: http://localhost:3000/image/{}/{}", s, test_image);
}
