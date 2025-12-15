local fileUtils = require("src.file_utils")

---@class Preview
---@field currentImageIdx integer defaults to 1
---@field allImages love.Image[]?
---@field zoom number current zoom level
---@field zoomMin number minimum zoom level
---@field zoomMax number maximum zoom level
---@field panX number pan offset X
---@field panY number pan offset Y
---@field dragging boolean whether currently dragging
---@field dragStartX number mouse X when drag started
---@field dragStartY number mouse Y when drag started
local Preview = {
  currentImageIdx = 1,
  allImages = {},
  zoom = 1,
  zoomMin = 1,
  zoomMax = 8,
  panX = 0,
  panY = 0,
  dragging = false,
  dragStartX = 0,
  dragStartY = 0
}


function Preview:new()
  local obj = setmetatable({}, self)
  self.__index = self
  return obj
end

--- Opens file dialog and appends selected images to self.allImages
function Preview:appendImages()
  local appendImage = function(fileData)
    local im = love.graphics.newImage(fileData)
    table.insert(self.allImages, im)
  end

  fileUtils.processFiles(appendImage)
end

--- Zoom image
function Preview:zoomImage(x, y)
  local zoomSpeed = 0.1
  self.zoom = self.zoom + y * zoomSpeed
  self.zoom = math.max(self.zoomMin, math.min(self.zoomMax, self.zoom))
end

function Preview:startDrag(x, y)
  self.dragging = true
  self.dragStartX = x - self.panX
  self.dragStartY = y - self.panY
end

function Preview:updateDrag(x, y)
  if self.dragging then
    self.panX = x - self.dragStartX
    self.panY = y - self.dragStartY
    self:clampPan()
  end
end

function Preview:clampPan()
  if not self.allImages or not self.allImages[self.currentImageIdx] then
    return
  end

  local preview_start = love.graphics.getWidth() * 0.15
  local preview_width = love.graphics.getWidth() - preview_start
  local preview_height = love.graphics.getHeight()

  local currImage = self.allImages[self.currentImageIdx]
  local img_width = currImage:getWidth()
  local img_height = currImage:getHeight()

  local scale_x = preview_width / img_width
  local scale_y = preview_height / img_height
  local base_scale = math.min(scale_x, scale_y)
  local scale = base_scale * self.zoom

  local scaled_width = img_width * scale
  local scaled_height = img_height * scale

  local maxPanX = math.max(0, (scaled_width - preview_width) / 2 + preview_width * 0.25)
  local maxPanY = math.max(0, (scaled_height - preview_height) / 2 + preview_height * 0.25)

  self.panX = math.max(-maxPanX, math.min(maxPanX, self.panX))
  self.panY = math.max(-maxPanY, math.min(maxPanY, self.panY))
end

function Preview:endDrag()
  self.dragging = false
end

function Preview:getTransform()
  local preview_start = love.graphics.getWidth() * 0.15
  local preview_width = love.graphics.getWidth() - preview_start
  local preview_height = love.graphics.getHeight()

  if self.allImages and self.allImages[self.currentImageIdx] then
    local currImage = self.allImages[self.currentImageIdx]
    local img_width = currImage:getWidth()
    local img_height = currImage:getHeight()

    local scale_x = preview_width / img_width
    local scale_y = preview_height / img_height
    local base_scale = math.min(scale_x, scale_y)
    local scale = base_scale * self.zoom

    local scaled_width = img_width * scale
    local scaled_height = img_height * scale

    local x = preview_start + (preview_width - scaled_width) / 2 + self.panX
    local y = (preview_height - scaled_height) / 2 + self.panY

    return { x = x, y = y, scale = scale }
  end
  return nil
end

function Preview:screenToImage(screenX, screenY)
  local transform = self:getTransform()
  if not transform then return nil, nil end
  local imgX = (screenX - transform.x) / transform.scale
  local imgY = (screenY - transform.y) / transform.scale
  return imgX, imgY
end

function Preview:draw()
  local transform = self:getTransform()
  if transform then
    local currImage = self.allImages[self.currentImageIdx]
    love.graphics.draw(currImage, transform.x, transform.y, 0, transform.scale, transform.scale)
  end
end

function Preview:incrementIdx()
  self.currentImageIdx = (self.currentImageIdx % #self.allImages) + 1
  self.zoom = 1
  self.panX, self.panY = 0, 0
end

return Preview
