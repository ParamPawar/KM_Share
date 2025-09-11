use webrtc::api::APIBuilder;
use webrtc::peer_connection::configuration::RTCConfiguration;
use webrtc::data_channel::data_channel_init::RTCDataChannelInit;

/// start a webrtc DataChannel connection
pub async fn start_webrtc() -> anyhow::Result<()> {
    let api = APIBuilder::new().build();
    let config = RTCConfiguration::default();

    let pc = api.new_peer_connection(config).await?;

    let dc = pc.create_data_channel("control", Some(RTCDataChannelInit::default())).await?;
    dc.on_open(Box::new(|| {
        Box::pin(async move {
            println!("✅ DataChannel open!");
        })
    }));

    dc.on_message(Box::new(move |msg| {
        Box::pin(async move {
            println!("📩 Got: {:?}", String::from_utf8(msg.data.to_vec()).unwrap());
        })
    }));

    Ok(())
}
