local Sidebar = require("src.ui.sidebar")
local Preview = require("src.ui.preview")
local Button = require("src.ui.button")
local Color = require("src.ui.colors")
local Annotations = require("src.ui.annotations")

function love.load()
  -- love.window.maximize()
  local font = love.graphics.newFont(16)
  font:setFilter("nearest", "nearest")
  love.graphics.setFont(font)
  love.graphics.setBackgroundColor(Color.BASE)
  love.keyboard.setTextInput(true)
  SizeAllCursor = love.mouse.getSystemCursor("sizeall")
  CorsshariCursor = love.mouse.getSystemCursor("crosshair")

  AppPreview = Preview:new()
  AppSidebar = Sidebar:new()
  AppAnnotations = Annotations:new()

  table.insert(
    AppSidebar.elements,
    Button:new(
      {
        x = 20,
        y = 20,
        text = "Open files",
        action_f = function() AppPreview:appendImages() end,
      }
    )
  )

  table.insert(
    AppSidebar.elements,
    Button:new(
      {
        x = 20,
        y = 70,
        text = "Next image",
        action_f = function() AppPreview:incrementIdx() end,
      }
    )
  )
end

function love.update(dt)
  AppSidebar:update()
  local mx, my = love.mouse.getPosition()
  local preview_start = love.graphics.getWidth() * 0.15

  if love.mouse.isDown(1) and mx > preview_start then
    local imgX, imgY = AppPreview:screenToImage(mx, my)
    if imgX then
      AppAnnotations:addPoint(imgX, imgY)
    end
  end

  if love.mouse.isDown(2) then
    AppPreview:updateDrag(mx, my)
  end
end

function love.mousepressed(x, y, button)
  local preview_start = love.graphics.getWidth() * 0.15
  if button == 1 and x > preview_start then
    love.mouse.setCursor(CorsshariCursor)
    local imgX, imgY = AppPreview:screenToImage(x, y)
    if imgX then
      AppAnnotations:startPolygon(AppPreview.currentImageIdx, imgX, imgY)
    end
  elseif button == 2 then
    love.mouse.setCursor(SizeAllCursor)
    AppPreview:startDrag(x, y)
  end
end

function love.mousereleased(x, y, button)
  if button == 1 then
    AppAnnotations:endPolygon()
  elseif button == 2 then
    AppPreview:endDrag()
  end
  love.mouse.setCursor()
end

function love.wheelmoved(x, y)
  AppPreview:zoomImage(x, y)
end

function love.draw()
  AppPreview:draw()

  local transform = AppPreview:getTransform()
  if transform then
    AppAnnotations:draw(AppPreview.currentImageIdx, transform)
  end

  AppSidebar:draw()
end
