import chess
from transformers import LlamaTokenizerFast, LlamaForCausalLM
from llabot import logger

class ChessLLM:
    def __init__(self, difficulty_level="normal", log_file="chess_llama.log"):
        # Set up logging
        self.setup_logging(log_file)
        
        # Initialize board and variables
        self.board = chess.Board()
        self.moves_uci = []
        self.difficulty_level = difficulty_level
        
        # Load model and tokenizer
        self.tokenizer = LlamaTokenizerFast.from_pretrained('lazy-guy12/chess-llama')
        self.model = LlamaForCausalLM.from_pretrained('lazy-guy12/chess-llama')

        # Difficulty settings (Temperature, Top_k, Max retries)
        self.difficulty_settings = {
            "very_easy": {"temperature": 1.0, "top_k": 100, "retries": 100},
            "easy": {"temperature": 0.8, "top_k": 75, "retries": 75},
            "normal": {"temperature": 0.6, "top_k": 50, "retries": 50},
            "intermediate": {"temperature": 0.4, "top_k": 30, "retries": 30},
            "hard": {"temperature": 0.2, "top_k": 20, "retries": 20},
        }

    def get_difficulty_params(self):
        return self.difficulty_settings.get(self.difficulty_level, self.difficulty_settings["normal"])

    def submit_player_move(self, move_uci: str) -> bool:
        """
        Submits a player's move if valid.
        :param move_uci: The player's move in UCI format.
        :return: True if the move is valid and successfully submitted, False otherwise.
        """
        try:
            move = chess.Move.from_uci(move_uci)
            if self.board.is_legal(move):
                self.board.push(move)
                self.moves_uci.append(move_uci)
                logger.info(f"Player move submitted: {move_uci}")
                return True
            else:
                logger.warning(f"Player move {move_uci} is illegal.")
        except ValueError:
            logger.warning(f"Invalid move format: {move_uci}")
        return False

    def play_llama(self) -> str:
        """
        Generates and submits the AI's move if valid.
        :return: The AI's move in UCI format, or "0000" if no valid move is found.
        """
        input_text = "1-0 " + " ".join(self.moves_uci)
        logger.debug(f"AI Input Moves (UCI): {input_text}")
        inputs = self.tokenizer(input_text, return_tensors="pt")
        
        params = self.get_difficulty_params()
        temperature = params["temperature"]
        top_k = params["top_k"]
        max_retries = params["retries"]

        for attempt in range(max_retries):
            generated = self.model.generate(
                input_ids=inputs['input_ids'],
                max_new_tokens=5,
                do_sample=True,
                top_k=top_k,
                temperature=temperature,
            )
            
            generated_move_full = self.tokenizer.decode(generated[0], skip_special_tokens=True)
            logger.debug(f"Attempt {attempt + 1} - Full Generated Move: {generated_move_full}")
            
            move_index = len(self.moves_uci) + 1
            generated_move = generated_move_full.split()[move_index] if len(generated_move_full.split()) > move_index else ""
            logger.debug(f"Attempt {attempt + 1} - Trimmed Move (UCI): {generated_move}")
            
            try:
                move = chess.Move.from_uci(generated_move)
                if self.board.is_legal(move):
                    self.board.push(move)
                    self.moves_uci.append(generated_move)
                    logger.info(f"AI move submitted: {generated_move}")
                    return generated_move
                else:
                    logger.debug(f"Move {generated_move} is illegal.")
            except ValueError:
                logger.debug(f"Invalid move format: {generated_move}")
        
        logger.error("AI failed to generate a valid move after all retries.")
        return "0000"

    def get_valid_moves(self) -> dict:
        return {move.uci(): move for move in self.board.legal_moves}

    def get_move_history(self) -> list:
        return [move.uci() for move in self.board.move_stack]