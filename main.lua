function love.load()
	X, Y, W, H = 20, 20, 60, 20
end

function love.update(dt)
	W = W + 1
	H = H + 1
end

function love.draw()
	love.graphics.setColor(0, 0.4, 0.4)
	love.graphics.rectangle("fill", X, Y, W, H)
end
