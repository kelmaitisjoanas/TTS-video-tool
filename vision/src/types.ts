export interface AudioSegment {
  id: string;
  url: string;
  text: string;
  duration: number;
  wordTimings: { word: string; start: number; end: number }[];
  srtUrl?: string;
}

export interface VisualAsset {
  id: string;
  url: string;
  type: 'image' | 'video';
  startTime: number; // Seconds from start of project
  transition: 'fade' | 'slide' | 'zoom' | 'blur' | 'rotate' | 'bounce' | 'skew' | 'none';
}

export interface ProjectState {
  audioSegments: AudioSegment[];
  visualAssets: VisualAsset[];
  isPlaying: boolean;
  currentTime: number;
  totalDuration: number;
}
