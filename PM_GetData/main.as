// Data Sending Plugin for Trackmania to {Python || other kind} Server

// --- Buffer Writing Functions ---
bool send_memory_buffer(Net::Socket@ sock, MemoryBuffer@ buf) {
    if (!sock.Write(buf)) {
        print("INFO: Disconnected, could not send data.");
        return false;
    }
    return true;
}

void append_float(MemoryBuffer@ buf, float val) {
    buf.Write(val);
}

void append_bool(MemoryBuffer@ buf, bool val) {
    uint8 byte_val = val ? 1 : 0;
    buf.Write(byte_val);
}

void Main() {
    print("Starting plugin as TCP Client...");

    auto sock = Net::Socket();
    MemoryBuffer@ buf = MemoryBuffer(0);

    float prev_speed = 0;
    float prev_accel = 0;

    while (true) {
        
        print("⌛ Trying to connect to Python Server on 127.0.0.1:9000...");
        
        if (!sock.Connect("127.0.0.1", 9000)) {
            print("❌ Connection failed. Retrying in 5 seconds...");
            sock.Close(); 
            sleep(5000); 
            continue;
        }
        
        print("✅ Connected to Python Server.");

        while (!sock.CanWrite()) yield(); 
        print("🟢 Ready to send data...");

        while (true) {
            CTrackMania@ app = cast<CTrackMania>(GetApp());
            if (app is null) { yield(); continue; }

            CSmArenaClient@ playground = cast<CSmArenaClient>(app.CurrentPlayground);
            if (playground is null) { yield(); continue; }

            CSceneVehicleVisState@ vehicle = VehicleState::ViewingPlayerState();
            if (vehicle is null) { yield(); continue; }

            auto race_state = playground.GameTerminals[0].UISequence_Current;

            float speed = vehicle.FrontSpeed;
            float accel = speed - prev_speed;
            float jerk = accel - prev_accel;
            prev_speed = speed;
            prev_accel = accel;

            bool isFinished = (race_state == SGamePlaygroundUIConfig::EUISequence::Finish
                || race_state == SGamePlaygroundUIConfig::EUISequence::EndRound);

            buf.Seek(0, 0); 
            append_float(buf, speed);
            append_float(buf, accel);
            append_float(buf, jerk);
            append_bool(buf, isFinished);
            buf.Seek(0, 0); 

            if (!send_memory_buffer(sock, buf)) {
                print("🔴 Disconnected from server.");
                break; 
            }

            yield(); 
        }
        sock.Close();
        print("🧹 Socket closed, retrying connection...");
    }
}