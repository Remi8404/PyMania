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

void append_uint(MemoryBuffer@ buf, uint val) {
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

    while (true) {
        
        print("Trying to connect to Local Server on 127.0.0.1:9000...");
        
        if (!sock.Connect("127.0.0.1", 9000)) {
            print("Connection failed. Retrying in 5 seconds...");
            sock.Close(); 
            sleep(5000); 
            continue;
        }
        
        print("Connected to Local Server : '127.0.0.1:9000' .");

        while (!sock.IsReady()) yield(); 
        print("Ready to send data...");
        CTrackMania@ app = cast<CTrackMania>(GetApp());
        if (app is null) { yield(); continue; }

        CSmArenaClient@ playground = cast<CSmArenaClient>(app.CurrentPlayground);
        
        if (playground is null) { yield(); continue; }
        CSmArena@ arena = cast<CSmArena>(playground.Arena);
        if(arena is null) { yield(); continue; }
		if(arena.Players.Length <= 0) { yield(); continue; }
        auto player = arena.Players[0];
		if(player is null) { yield(); continue; }
        CSmScriptPlayer@ api = cast<CSmScriptPlayer>(player.ScriptAPI);
		if(api is null) { yield(); continue; }

        while (true) {
            CSceneVehicleVisState@ vehicle = VehicleState::ViewingPlayerState();
            if (vehicle is null) { yield(); continue; }

            auto race_state = playground.GameTerminals[0].UISequence_Current;

            float speed = vehicle.FrontSpeed * 3.6;
            float accel = speed - prev_speed;
            prev_speed = speed;

            vec3 dir = vehicle.Dir;
            vec3 up = vehicle.Up;
            vec3 left = vehicle.Left;

            float yaw =  Math::Atan2( dir.z, -dir.x ); 
            float pitch = Math::Atan2( dir.y, Math::Sqrt(Math::Pow(dir.x, 2) + Math::Pow(dir.z, 2)));
            float roll = Math::Atan2( left.y, up.y);

            bool flOnGround = (vehicle.FLGroundContactMaterial != EPlugSurfaceMaterialId::XXX_Null);
            bool frOnGround = (vehicle.FRGroundContactMaterial != EPlugSurfaceMaterialId::XXX_Null);
            bool rlOnGround = (vehicle.RLGroundContactMaterial != EPlugSurfaceMaterialId::XXX_Null);
            bool rrOnGround = (vehicle.RRGroundContactMaterial != EPlugSurfaceMaterialId::XXX_Null);

           uint startTime = vehicle.RaceStartTime;

            bool isFinished = (race_state == SGamePlaygroundUIConfig::EUISequence::Finish
                || race_state == SGamePlaygroundUIConfig::EUISequence::EndRound);

            buf.Seek(0, 0); 
            append_float(buf, speed);
            append_float(buf, accel);
            append_float(buf, VehicleState::GetSideSpeed(vehicle) * 3.6);
            append_float(buf, yaw);
            append_float(buf, pitch);
            append_float(buf, roll);
            append_bool(buf, flOnGround);
            append_bool(buf, frOnGround);
            append_bool(buf, rlOnGround);  
            append_bool(buf, rrOnGround);
            append_uint(buf, startTime);
            append_bool(buf, isFinished);
            buf.Seek(0, 0); 

            if (!send_memory_buffer(sock, buf)) {
                print("Disconnected from server.");
                break; 
            }

            yield(); 
        }
        sock.Close();
        print("Socket closed, retrying connection...");
    }
}