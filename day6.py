#!/usr/bin/env python3
import fileinput

START_PACKET_MARKER_LENGTH = 4
START_MESSAGE_MARKER_LENGTH = 14

def find_start_position(input: str, marker_length: int) -> int:
    for i in range(len(input) - (marker_length - 1)):
        marker = input[i:i + marker_length]
        if len(set(marker)) == marker_length:
            return i + marker_length

if __name__ == '__main__':
    datastream_buffer = fileinput.input().readline()

    # part 1
    assert find_start_position('mjqjpqmgbljsphdztnvjfqwrcgsmlb', START_PACKET_MARKER_LENGTH) == 7
    assert find_start_position('bvwbjplbgvbhsrlpgdmjqwftvncz', START_PACKET_MARKER_LENGTH) == 5
    assert find_start_position('nppdvjthqldpwncqszvftbrmjlhg', START_PACKET_MARKER_LENGTH) == 6
    assert find_start_position('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', START_PACKET_MARKER_LENGTH) == 10
    assert find_start_position('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', START_PACKET_MARKER_LENGTH) == 11

    packet_start_position = find_start_position(datastream_buffer, START_PACKET_MARKER_LENGTH)
    print(f"Packet start position: {packet_start_position}")

    # part 2
    assert find_start_position('mjqjpqmgbljsphdztnvjfqwrcgsmlb', START_MESSAGE_MARKER_LENGTH) == 19
    assert find_start_position('bvwbjplbgvbhsrlpgdmjqwftvncz', START_MESSAGE_MARKER_LENGTH) == 23
    assert find_start_position('nppdvjthqldpwncqszvftbrmjlhg', START_MESSAGE_MARKER_LENGTH) == 23
    assert find_start_position('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', START_MESSAGE_MARKER_LENGTH) == 29
    assert find_start_position('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', START_MESSAGE_MARKER_LENGTH) == 26

    message_start_position = find_start_position(datastream_buffer, START_MESSAGE_MARKER_LENGTH)
    print(f"Message start position: {message_start_position}")
