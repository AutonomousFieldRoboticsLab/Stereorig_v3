#!/bin/bash

sshpass -p "AFRL1D49." ssh -p 22  afrl@192.168.0.150 'docker stop $(docker ps -a -q); systemctl --user stop docker-container.service; docker stop $(docker ps -a -q)'
sshpass -p "AFRL1D49." ssh -p 22  afrl@192.168.0.100 'docker stop $(docker ps -a -q); systemctl --user stop docker-container.service; docker stop $(docker ps -a -q)'

mkdir jetson_data

cd jetson_data

mkdir jetson_1

cd jetson_1

echo "Pulling data from jetson_1"
sshpass -p "AFRL1D49." scp -P 22 -r afrl@192.168.0.150:/home/afrl/Desktop/data .

cd .. && mkdir jetson_2

cd jetson_2

echo "Pulling data from jetson_2"
sshpass -p "AFRL1D49." scp -P 22 -r afrl@192.168.0.100:/home/afrl/Desktop/data .

cd ..

source /opt/ros/humble/setup.bash

cd jetson_data

for file in $(find . -type f); do 
    echo "Checking $file"

    # Step 1: Check the database with ros2 bag info
    source /opt/ros/humble/setup.bash
    ROS2_OUTPUT=$(ros2 bag info "$file" 2>&1)

    if echo "$ROS2_OUTPUT" | grep -q "No storage id specified"; then
        echo "Error detected in $file, starting repair process..."

        # Extract the filename from the full path
        filename=$(basename "$file")

        # Navigate to the directory containing the file
        FILE_DIR=$(dirname "$file")
        cd "$FILE_DIR"

        # Backup the original database
        echo "Backing up the original database..."
        cp "$filename" "$filename.bak"

        # Open the database in SQLite3 and dump all data
        echo "Dumping the database..."
        sqlite3 "$filename" <<EOF
.mode insert
.output dump_all.sql
.dump
.exit
EOF

        # Edit the SQL dump file to remove transaction commands
        echo "Modifying the SQL dump file..."
        { echo "PRAGMA synchronous = OFF;"; cat dump_all.sql; } | grep -v -e TRANSACTION -e ROLLBACK -e COMMIT > dump_all_notrans.sql

        # Create a new database and load the modified SQL dump into it
        echo "Creating a new database and loading data..."
        rm "$filename"
        sqlite3 "$filename" ".read dump_all_notrans.sql"

        # Verify the size of the new database
        echo "Verifying the new database size..."
        NEW_DB_SIZE=$(stat -c%s "$filename")
        echo "New database size: $NEW_DB_SIZE bytes"

        # Check the new database with ros2 bag info again
        ros2 bag info "$filename"

        echo "Database repair process completed for $filename."

        # Navigate back to the jetson_data directory
        cd - > /dev/null
    else
        echo "No errors detected in $file, skipping repair."
    fi
done

