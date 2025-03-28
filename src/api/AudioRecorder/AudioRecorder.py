import time
import pynput
import audiomath as am  

class MyListener(pynput.keyboard.Listener):
    def __init__(self, filename=None, buffer_length_seconds=10):
        """
        Note:
        
        If you specify a long enough `buffer_length_seconds` for your
        purposes, then you do not need to record to file and so do not
        need to specify `filename`.
        
        If you specify `filename`, you need to have installed `ffmpeg`
        (see the help for `audiomath.ffmeg.Install`).
        """
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None
        
        self.queue = []
        self.filename = filename
        self.buffer_length_seconds = buffer_length_seconds
        self.new_recorder()
        
    def new_recorder( self ):
        self.buffer = am.Sound(self.buffer_length_seconds, nChannels=2, fs=44100)
        self.recorder = am.Recorder(self.buffer, loop=True, recording=False, filename=self.filename)
        
    def on_press(self, key):
        try: key.char
        except: return
        if key.char == 'r' and not self.key_pressed:
            print('recording...')
            self.recorder.Record()
            self.key_pressed = True
        return True

    def on_release(self, key):
        try: key.char
        except: return
        if key.char == 'r' and self.key_pressed:
            print('finished')
            self.recorder.Stop()
            self.recorder = None # seems to be necessary when filename is used, to ensure the ffmpeg process and file are closed and cleaned up
            if self.filename:
                player = am.Player( self.filename )
            else:
                player = am.Player( self.buffer )
                # self.buffer.Write( 'output.wav')  # if you want to ensure every attempt gets saved. File will be overwritten.
            self.queue.append( player )
            self.new_recorder()
            self.key_pressed = False
        return True



if __name__ == "__main__":
    with MyListener('assets/temp/temp_record.wav') as listener:  # this variant uses a file (and needs ffmpeg)
    # with MyListener() as listener:               # this variant just records to memory
        while True:
            if listener.queue:
                player = listener.queue.pop( 0 )
                # player.Play()
            time.sleep(0.1)