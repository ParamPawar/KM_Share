use mdns::{RecordKind, Error};
use futures::StreamExt;
use std::time::Duration;
use tracing::info;

/// findother peers on LAN using mDNS
pub async fn discover_service() -> Result<(), Error> {
    let stream = mdns::discover::all("Smart_KVM._udp", Duration::from_secs(15))?
        .listen();

    tokio::pin!(stream);

    while let Some(Ok(event)) = stream.next().await {
        for record in event.records() {
            if let RecordKind::A(addr) = record.kind {
                info!("Discovered peer: {:?}", addr);
            }
        }
    }
    Ok(())
}

/// show device on LAN
pub fn advertise_service() -> Result<mdns::Service, Error> {
    mdns::Service::new("Smart_KVM._udp", 8080)
}
