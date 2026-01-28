import os
import math
from pydub import AudioSegment


def split_wav_by_size(file_path, max_size_mb=95):
    """
    WAVファイルを指定したサイズ（MB）以下に分割する。
    """
    if not os.path.exists(file_path):
        print(f"エラー: ファイル {file_path} が見つかりません。")
        return

    # 音声ファイルの読み込み
    audio = AudioSegment.from_wav(file_path)

    # 出力ディレクトリの作成
    output_dir = "split_chunks"
    os.makedirs(output_dir, exist_ok=True)

    # バイトレートから1ミリ秒あたりのバイト数を算出
    # (frame_rate * sample_width * channels) / 1000
    bytes_per_ms = (audio.frame_rate * audio.sample_width * audio.channels) / 1000

    # ターゲットサイズに相当する時間を計算
    target_size_bytes = max_size_mb * 1024 * 1024
    chunk_length_ms = math.floor(target_size_bytes / bytes_per_ms)

    # 分割実行
    print(f"分割を開始します: {file_path}")
    for i, start_ms in enumerate(range(0, len(audio), chunk_length_ms)):
        chunk = audio[start_ms : start_ms + chunk_length_ms]
        chunk_name = os.path.join(output_dir, f"chunk_{i+1}.wav")

        # 書き出し
        chunk.export(chunk_name, format="wav")
        print(f"保存完了: {chunk_name} ({len(chunk)/1000:.2f}秒)")


if __name__ == "__main__":
    # 実行（ファイル名は適宜変更してください）
    split_wav_by_size("./20260128_voicedata.wav")
