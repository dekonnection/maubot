// maubot - A plugin-based Matrix bot system.
// Copyright (C) 2018 Tulir Asokan
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.
import React from "react"

const Log = ({ lines, showName = true }) => <div className="log">
    {lines.map(data =>
        <div className="row" key={data.id}>
            <span className="time">{data.time.toLocaleTimeString()}</span>
            <span className="level">{data.levelname}</span>
            {showName && <span className="logger">{data.name}</span>}
            <span className="text">{data.msg}</span>
        </div>,
    )}
</div>

export default Log
