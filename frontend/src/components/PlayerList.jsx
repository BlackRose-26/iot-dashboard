import { Link } from 'react-router-dom'
import { Avatar, Badge } from './ui'
export default function PlayerList({ players, compact = false }) {
  return (
    <ol className={`player-list ${compact ? 'compact' : ''}`}>
      {players.map((p, i) => (
        <li key={p.code}>
          <span className={`rank ${i === 0 ? 'first' : ''}`}>
            {String(p.rank).padStart(2, '0')}
          </span>
          <Avatar name={p.nickname} index={i} />
          <div className="player-info">
            <strong>{p.nickname}</strong>
            <span>{p.code}</span>
          </div>
          <div className="player-score">
            <strong>
              {p.score.toLocaleString()}
              <small> pts</small>
            </strong>
            <span>
              Level {p.level} · {p.duration}s
            </span>
          </div>
        </li>
      ))}
    </ol>
  )
}
